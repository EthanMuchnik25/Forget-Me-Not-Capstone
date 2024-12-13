import torch

def modify_specific_names(model_path, name_mapping, output_path=None):
    """
    Modify specific class names in a YOLO .pt model file while keeping others unchanged
    
    Args:
        model_path (str): Path to the input YOLO .pt model
        name_mapping (dict): Dictionary mapping old names to new names
        output_path (str, optional): Path to save modified model. If None, overwrites input
    """
    # Load the model
    model = torch.load(model_path, map_location=torch.device('cpu'))
    
    def update_names(names):
        """Helper function to update names using the mapping"""
        if isinstance(names, dict):
            # Handle dictionary format (index to name mapping)
            return {k: name_mapping.get(v, v) for k, v in names.items()}
        elif isinstance(names, (list, tuple)):
            # Handle list format
            return [name_mapping.get(name, name) for name in names]
        return names

    # Find and update names based on model structure
    if isinstance(model, dict):
        if 'model' in model:
            # Handle newer YOLO format
            if hasattr(model['model'], 'names'):
                model['model'].names = update_names(model['model'].names)
            elif 'names' in model:
                model['names'] = update_names(model['names'])
        else:
            # Handle older format
            if 'names' in model:
                model['names'] = update_names(model['names'])
    else:
        # Handle model object format
        if hasattr(model, 'names'):
            model.names = update_names(model.names)
    
    # Save the modified model
    if output_path is None:
        output_path = model_path
    torch.save(model, output_path)
    print(f"Model saved with updated names to: {output_path}")
    
    # Display the current class names
    current_names = None
    if isinstance(model, dict):
        if 'model' in model and hasattr(model['model'], 'names'):
            current_names = model['model'].names
        elif 'names' in model:
            current_names = model['names']
    elif hasattr(model, 'names'):
        current_names = model.names
    
    if current_names:
        print("\nCurrent class names:")
        if isinstance(current_names, dict):
            for idx, name in current_names.items():
                print(f"Class {idx}: {name}")
        else:
            for idx, name in enumerate(current_names):
                print(f"Class {idx}: {name}")

# Example usage
if __name__ == "__main__":
    # Example model path
    model_path = "/mnt/c/Users/ethanm/Documents/18500/Forget-Me-Not-Capstone/webserver/app/model/binaries/best2.pt"
    
    # Define mapping of old names to new names
    # Only specify the names you want to change
    name_mapping = {
        'pencil - v1 2022-04-21 11-44am': 'pencil',
        'car': 'vehicle'
        # Add more mappings as needed
    }
    
    try:
        modify_specific_names(model_path, name_mapping)
        print("Names successfully modified!")
    except Exception as e:
        print(f"Error occurred: {str(e)}")