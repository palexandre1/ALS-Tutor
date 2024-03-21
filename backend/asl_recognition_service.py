import tensorflow as tf
import numpy as np

MODEL_PATH = "asl_model.keras"

class _ASL_Recognition_Service:

  model = None
  _classNames = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
  _instance = None

  def predict(self, imgURL):

    img_height = 64
    img_width = 64

    #load image into PIL format
    img = tf.keras.utils.load_img(
    imgURL, target_size=(img_height, img_width), keep_aspect_ratio=True
    )
    img_array = tf.keras.utils.img_to_array(img)
    print("Array for: ", imgURL, " ", img_array)
    img_array = tf.expand_dims(img_array, 0) # Create a batch
    print(img_array)

    #make predicition
    predictions = self.model.predict(img_array)
    print("Predictions are: ", predictions)
    score = tf.nn.softmax(predictions[0])
    predicted_letter = self._classNames[np.argmax(score)]


    return predicted_letter

def ASL_Recognition_Service():

  #confirm  that there is only 1 instance of ASL
  if _ASL_Recognition_Service._instance is None:
    _ASL_Recognition_Service._instance = _ASL_Recognition_Service()
    _ASL_Recognition_Service.model = tf.keras.models.load_model(MODEL_PATH)
  return _ASL_Recognition_Service._instance

if __name__ == "__main__":

  asl = ASL_Recognition_Service()

  # letterA = asl.predict("a.png")
  # letterB = asl.predict("b.png")
  # letterC = asl.predict("c.png")
  # letterL = asl.predict("l.png")
  # letterY = asl.predict("y.png")
  # letterCustom = asl.predict("snapshot.jpeg")

  print(f"Predicted keywords: {letterA}, {letterB}, {letterC}, {letterL}, {letterY}")
