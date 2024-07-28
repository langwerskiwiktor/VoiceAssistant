import wikipedia
import wolframalpha
import wx
import pyttsx3
import speech_recognition as sr

engine = pyttsx3.init()


class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None,
                          pos=wx.DefaultPosition, size=wx.Size(450, 100),
                          style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION |
                          wx.CLOSE_BOX | wx.CLIP_CHILDREN,
                          title="PyDa")
        panel = wx.Panel(self)
        my_sizer = wx.BoxSizer(wx.VERTICAL)
        lbl = wx.StaticText(
            panel, label="Hi, I am PyDa the Python Digital Assistan. How can I help you?")
        my_sizer.Add(lbl, 0, wx.ALL, 5)
        self.txt = wx.TextCtrl(
            panel, style=wx.TE_PROCESS_ENTER, size=(400, 30))
        self.txt.SetFocus()
        self.txt.Bind(wx.EVT_TEXT_ENTER, self.OnEnter)
        my_sizer.Add(self.txt, 0, wx.ALL, 5)
        panel.SetSizer(my_sizer)
        self.Show()

    def OnEnter(self, event):
        input_user = self.txt.GetValue()
        input_words = input_user.lower()
        if input_user == '':
            r = sr.Recognizer()
            with sr.Microphone() as source:
                engine.say("Proszę mówić teraz.")
                engine.runAndWait()
                audio = r.listen(source)
            try:
                recognized_text = r.recognize_google(audio, language='pl-PL')
                self.txt.SetValue(recognized_text)
                input_user = recognized_text
                input_words = input_user.lower()
            except sr.UnknownValueError:
                engine.say('Nie zrozumiałem, proszę spróbować ponownie.')
                engine.runAndWait()
                print('Google Speech Recognition could not understand audio')
                return
            except sr.RequestError as e:
                engine.say('Błąd połączenia z Google Speech Recognition.')
                engine.runAndWait()
                print(
                    f'Could not request results from Google Speech Recognition service; {e}')
                return
        else:
            try:
                app_id = "J2P6L3-H3432G6HA6"
                client = wolframalpha.Client(app_id)
                res = client.query(input_words)
                answer = next(res.results).text
                print(answer)
                engine.say("Odpowiedź to " + answer)
                engine.runAndWait()
            except (StopIteration, AttributeError):
                try:
                    engine.say(
                        "Nie znalazłem odpowiedzi w WolframAlpha. Szukam w Wikipedii " + input_user)
                    engine.runAndWait()
                    summary = wikipedia.summary(input_words, sentences=2)
                    print(summary)
                    engine.say("Odpowiedź to " + summary)
                    engine.runAndWait()
                except wikipedia.exceptions.DisambiguationError as e:
                    engine.say(
                        "Twoje zapytanie jest niejednoznaczne. Proszę podać więcej informacji.")
                    engine.runAndWait()
                    print("DisambiguationError: Proszę podać więcej informacji.")
                except wikipedia.exceptions.PageError:
                    engine.say("Nie znalazłem odpowiedzi na Twoje zapytanie.")
                    engine.runAndWait()
                    print("PageError: Nie znalazłem odpowiedzi na Twoje zapytanie.")
                except Exception as e:
                    engine.say("Wystąpił błąd podczas wyszukiwania.")
                    engine.runAndWait()
                    print(f"Exception: {e}")


if __name__ == "__main__":
    app = wx.App(True)
    frame = MyFrame()
    app.MainLoop()
