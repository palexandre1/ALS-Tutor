import tensorflow as tf
import numpy as np

MODEL_PATH = "asl_model.keras"

class _ASL_Recognition_Service:

  model = None
  _classNames = ['a','b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
               'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
               'y', 'z']
  _instance = None

  def predict(self, imgURL):

    img_height = 256
    img_width = 256

    #download image from image url
    # inputImg_path = tf.keras.utils.get_file('Input_image', origin=imgURL)

    #load image into PIL format
    img = tf.keras.utils.load_img(
    imgURL, target_size=(img_height, img_width)
    )
    img_array = tf.keras.utils.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0) # Create a batch

    #make predicition
    predictions = self.model.predict(img_array)
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

  letterA = asl.predict("a.jpeg")
  letterB = asl.predict("b.jpeg")
  letterC = asl.predict("c.jpeg")
  letterD = asl.predict("d.jpeg")
  letterE = asl.predict("e.jpeg")

  print(f"Predicted keywords: {letterA},{letterB},{letterC},{letterD},{letterE}")
