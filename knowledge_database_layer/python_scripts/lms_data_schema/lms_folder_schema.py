#SUBFOLDER IMPORT
from .lms_content.lms_content_schema import *
from .lms_data.lms_data_schema import *
from .lms_metadata.lms_metadata import *
from .lms_quizz_and_exams.lms_quizz_and_exams_schema import *


#LMS CONTENT COLLECTIONS IMPORTS
from .lms_content.lms_course import *
from .lms_content.lms_module import *
from .lms_content.lms_lessons import *
from .lms_content.lms_instructor import *
from .lms_content.lms_lesson_resources import *

#LMS QUIZZ AND EXAMS COLLECTIONS IMPORT

from .lms_quizz_and_exams.lms_question_bank import *
from .lms_quizz_and_exams.lms_quizz import *

#LMS DATA COLLECTIONS IMPORT
from .lms_data.lms_comments import *
from .lms_data.lms_courses_reviews import *
from .lms_data.lms_enrollement import *

#LMS METADATA COLLECTIONS IMPORT
from .lms_metadata.lms_settings import *
from .lms_metadata.lms_topic import *
from .lms_metadata.lms_tracks import *



#DEFINE ROOT FOLDER
lms_schema = {
	"collection": "lms",
	"meta": {
		"collection": "lms",
		"icon": "folder",
	},
	"schema": None,
}