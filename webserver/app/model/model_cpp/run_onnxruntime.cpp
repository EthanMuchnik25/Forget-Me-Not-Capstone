#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>
#include <onnxruntime/core/session/onnxruntime_cxx_api.h>
#include <opencv2/opencv.hpp>

// NOTE: instructions on how to get this to work in cpp_yolo_onnx.md. Getting it
//  to work requires downloading onnxruntime sdk, as well as some other weird
//  cmake stuff

namespace py = pybind11;

class YOLOModel {
public:
    YOLOModel(const std::string &model_path) {
        Ort::Env env(ORT_LOGGING_LEVEL_WARNING, "YOLOv11");
        session_options.SetGraphOptimizationLevel(GraphOptimizationLevel::ORT_ENABLE_EXTENDED);
        session = std::make_unique<Ort::Session>(env, model_path.c_str(), session_options);
        
        // Get input and output names
        input_name = session->GetInputName(0, allocator);
        output_name = session->GetOutputName(0, allocator);
    }

    py::array_t<float> run_yolo_cpp(py::handle file_handle) {
        // Read image from Python file-like object
        py::buffer_info buf = py::reinterpret_borrow<py::buffer>(file_handle).request();
        std::vector<uchar> img_data((uchar*)buf.ptr, (uchar*)buf.ptr + buf.size);
        cv::Mat image = cv::imdecode(img_data, cv::IMREAD_COLOR);

        // Preprocess image: resize and normalize
        const int input_size = 640;
        cv::resize(image, image, cv::Size(input_size, input_size));
        image.convertTo(image, CV_32F, 1.0 / 255.0);
        
        // Convert image to tensor format (N, C, H, W)
        std::vector<float> input_tensor_values(input_size * input_size * 3);
        std::memcpy(input_tensor_values.data(), image.data, input_tensor_values.size() * sizeof(float));

        // Create tensor for input data
        std::vector<int64_t> input_dims = {1, 3, input_size, input_size};
        Ort::Value input_tensor = Ort::Value::CreateTensor<float>(memory_info, input_tensor_values.data(), input_tensor_values.size(), input_dims.data(), input_dims.size());

        // Run inference
        auto output_tensors = session->Run(Ort::RunOptions{nullptr}, &input_name, &input_tensor, 1, &output_name, 1);
        float* floatarr = output_tensors[0].GetTensorMutableData<float>();

        // Assume output shape for YOLO (adjust as per model output)
        auto output_shape = output_tensors[0].GetTensorTypeAndShapeInfo().GetShape();
        py::array_t<float> result({output_shape[1], output_shape[2]}, floatarr);
        return result;
    }

private:
    Ort::SessionOptions session_options;
    Ort::AllocatorWithDefaultOptions allocator;
    std::unique_ptr<Ort::Session> session;
    const char *input_name;
    const char *output_name;
    Ort::MemoryInfo memory_info = Ort::MemoryInfo::CreateCpu(OrtArenaAllocator, OrtMemTypeDefault);
};

// PYBIND11_MODULE is a macro that creates a Python module
PYBIND11_MODULE(yolo_inference_cpp, m) {
    py::class_<YOLOModel>(m, "YOLOModel")
        .def(py::init<const std::string &>())
        .def("run_yolo_cpp", &YOLOModel::run_yolo_cpp);
}