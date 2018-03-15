'''
    This method checks whether student has any exam happening at the moment or not by communicating with server
    Accordingly, it enables or disables the text and button on PgStdLects
'''

from kivy.logger import Logger

from GUI.func import database_api

def check_std_live_exam(self, dt):
    try:
        # self.data_live_exam = TODO

        if self.data_live_exam is not None:
            self.ids["btn_join_exam"].disabled = False
            self.ids["txt_join_exam_name"].color = (1,1,1,1)
            self.ids["txt_join_exam_name"].text = "%s has started!" % self.data_live_exam

            Logger.info("check_std_live_exam: Successfully checked, there is a live exam")
        else:
            self.ids["btn_join_exam"].disabled = True
            self.ids["txt_join_exam_name"].color = (1,1,1,0.25)
            self.ids["txt_join_exam_name"].text = "No exam started"

            Logger.info("check_std_live_exam: Successfully checked, there is no live exam")
    except:
        Logger.error("check_std_live_exam: Server is not reachable")