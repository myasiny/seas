'''
    This method checks whether student has any exam happening at the moment or not by communicating with server
    Accordingly, it enables or disables the text and button on PgStdLects
'''

from kivy.logger import Logger

from SEAS.func import database_api

def check_std_live_exam(self, dt):
    try:
        self.live_exam = None

        self.data_live_exam = database_api.getExamsOfLecture(self.data_login[8].replace("\n", ""), self.ids["txt_lect_code"].text)

        for exam in self.data_live_exam:
            if exam[5] == "active":
                self.live_exam = exam[1]

                self.ids["txt_info_head"].text = self.live_exam.title()

                self.ids["img_join_exam_name"].opacity = 1
                self.ids["btn_join_exam"].disabled = False
                self.ids["txt_join_exam_name"].color = (1,1,1,1)
                self.ids["txt_join_exam_name"].text = "%s has started!" % self.ids["txt_info_head"].text

                Logger.info("check_std_live_exam: Successfully checked, there is a live exam")
                break
            else:
                self.live_exam = None

        if self.live_exam is None:
            self.ids["img_join_exam_name"].opacity = 0.1
            self.ids["btn_join_exam"].disabled = True
            self.ids["txt_join_exam_name"].color = (1,1,1,0.25)
            self.ids["txt_join_exam_name"].text = "No exam started"

            Logger.info("check_std_live_exam: Successfully checked, there is no live exam")
    except:
        Logger.error("check_std_live_exam: Server is not reachable")