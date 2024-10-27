
Currently:
blocklist
-> blocklist tokens are only removed when they expire, not necessarily when the user gets deleted.





With proper auth, we may not want plaintext stored on the raspberry pi

KISS:
Easy way to implement logout is boot out all tickets made before a certain date
-> I think I will do this for testing purposes for now

Behavioral notes:
We may ideally want to give the raspis tokens with very long expiration dates.
-> as long as we don't change our generation key the tokens should still be valid
-> In practice, I am guessing the server has some way to send keys to the device
so that it can rotate keys, no one gets hacked.

Implementation notes:
-> Later, may want a more complicated scheme with blacklists
 -> Would want to be able to clear out blacklists every once in a while
  -> remove tokens that would have expired anyways
  -> regenerate all tokens every once in a while for full reset
-> Need to give cameras a way to:
 -> stay connected all the time
 -> change account, but not have camera still have access to old thing
 -> if we just delete the token, it should be impossible to regenerate
  -> however malicious actor could still sue to send pics
   -> recycle scheme should fix this
-> Advanced: Arbitrary associations of users with cameras
 -> Cameras are identifiable, and can be made to correspond with an account
 -> Construct of household
  -> household has admin
   -> can update policies of which household members can be allowed to see which 
cameras
  -> cameras are associated with a household
   -> within website, user can pick which cameras it has access to to query from


TODO: decide necessary policy
-> token timeout