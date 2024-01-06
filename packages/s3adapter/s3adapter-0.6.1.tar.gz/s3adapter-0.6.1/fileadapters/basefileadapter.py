from abc import ABC, abstractmethod
#from formaters import basefileformater

#TODO: [SCRUM-16] S3Adapter - Future Implementation of BaseFileAdapter Abstract Base Class to Adapters
class basefileadapter(ABC):
  def __init__(self, file_path, file_name):  
    #init base adapter class
    self.file_path = file_path
    self.file_name = file_name
    #self.formater = formater
  
  @abstractmethod
  def read(self):
    pass

  @abstractmethod
  def write(self):
    pass

  @abstractmethod
  def write(self, file_path, file_name):
    pass

  @abstractmethod
  def exist(self):
    pass

    
