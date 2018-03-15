'''
    This method checks whether student has any exam happening at the moment or not by communicating with server
    Accordingly, it enables or disables the text and button on PgStdLects
'''

from kivy.logger import Logger

from GUI.func import database_api

def check_std_live_exam(self, dt):
    try:
        live_exam = False

        self.data_live_exam = database_api.getExamsOfLecture(self.data_login[8].replace("\n", ""), self.ids["txt_lect_code"].text)

        for exam in self.data_live_exam:
            if exam[5] == "active":
                live_exam = True

                self.ids["btn_join_exam"].disabled = False
                self.ids["txt_join_exam_name"].color = (1,1,1,1)
                self.ids["txt_join_exam_name"].text = "%s has started!" % self.data_live_exam

                Logger.info("check_std_live_exam: Successfully checked, there is a live exam")

                break

        if not live_exam:
            self.ids["btn_join_exam"].disabled = True
            self.ids["txt_join_exam_name"].color = (1,1,1,0.25)
            self.ids["txt_join_exam_name"].text = "No exam started"

            Logger.info("check_std_live_exam: Successfully checked, there is no live exam")
    except:
        Logger.error("check_std_live_exam: Server is not reachable")