import tkinter

class MainWindow(tkinter.Frame):
  def __init__(self, parent) -> None:
      super(MainWindow, self).__init__(parent)
      self.parent = parent
      self.grid(row=0, column=0, sticky=tkinter.NSEW)      
      self.init_ui()

  def init_ui(self) -> None:
      # creating widgets
      from tkinter import Button, Label, Spinbox
      button_input = Button(self, text='Open video', command=self.set_input)
      button_input.focus_set()
      self.label_input = Label(self, relief=tkinter.SUNKEN)
      button_output = Button(self, text='Saving directory', command=self.set_output)
      self.label_output = Label(self, relief=tkinter.SUNKEN)
      label_everyno1 = Label(self, text='Save only every ', relief=tkinter.GROOVE, anchor=tkinter.E)
      self.spinbox_everyno = Spinbox(self, from_=1, to=100, textvariable=tkinter.DoubleVar(value=2))
      label_everyno2 = Label(self, text='frame', relief=tkinter.GROOVE, anchor=tkinter.W)
      button_do = Button(self, text='Save frames', command=self.do)
      self.label_do = Label(self, relief=tkinter.GROOVE)
      button_quit = Button(self, text='Quit', command=self.quit)

      # placing in grid
      button_input.grid(row=0, column=0, padx=3, pady=3, sticky=tkinter.NSEW)
      self.label_input.grid(row=0, column=1, columnspan=2, padx=3, pady=3, sticky=tkinter.NSEW)
      button_output.grid(row=1, column=0, padx=3, pady=3, sticky=tkinter.NSEW)
      self.label_output.grid(row=1, column=1, columnspan=2, padx=3, pady=3, sticky=tkinter.NSEW)
      label_everyno1.grid(row=2, column=0, padx=3, pady=3, sticky=tkinter.NSEW)
      self.spinbox_everyno.grid(row=2, column=1, padx=3, pady=3, sticky=tkinter.NSEW)
      label_everyno2.grid(row=2, column=2, padx=3, pady=3, sticky=tkinter.NSEW)
      button_do.grid(row=3, column=0, padx=3, pady=3, sticky=tkinter.NSEW)
      self.label_do.grid(row=3, column=1, columnspan=2, padx=3, pady=3, sticky=tkinter.NSEW)
      button_quit.grid(row=4, column=2, padx=3, pady=3, sticky=tkinter.E)

      self.columnconfigure(0, weight=0)
      self.columnconfigure(1, weight=2)
      self.columnconfigure(2, weight=1)

  def set_input(self) -> None:
    from tkinter import filedialog as fd
    self.label_input['text'] = fd.askopenfilename()

  def set_output(self) -> None:
    from tkinter import filedialog as fd
    self.label_output['text'] = fd.askdirectory()

  def do(self) -> None:
    # opencv-python
    import cv2
    from tkinter.messagebox import showinfo
    from os.path import basename
    
    video_in, dir_out = self.label_input['text'], self.label_output['text']
    if not video_in or not dir_out:
      showinfo(title='To images', message='No input or output')
      return None
    
    frame_no = -1
    fname = basename(video_in)
    cap = cv2.VideoCapture(video_in)
    # success,image = cap.read()
    while True:
      for i in range(0, int(self.spinbox_everyno.get())):
        success,image = cap.read()
        if not success:
          break;
        frame_no += 1
      if success:
        iname = f'{dir_out}/{fname}_frame_{frame_no}.jpg'
        cv2.imwrite(iname, image)
        self.label_do['text'] = f'frame {frame_no}'
        self.update()
      else:
        showinfo(title='Save frames', message='Done')
        break
    cv2.destroyAllWindows()

  def quit(self, event=None) -> None:
    self.parent.destroy()

if __name__ == '__main__':
  app = tkinter.Tk()
  app.title('Video to images')
  app.minsize(width=300, height=150)
  app.resizable(True,False)
  app.eval('tk::PlaceWindow . center')
  app.rowconfigure(0, weight=1)
  app.columnconfigure(0, weight=1)
  mw = MainWindow(app)
  app.protocol('WM_DELETE_WINDOW', mw.quit)
  app.mainloop()
