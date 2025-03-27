
lms_question_bank = {
	"collection": "lms_question_bank",
	"meta": {
		"collection": "lms_question_bank",
        "group": "lms_quizz_and_exams",
		"icon": "question_mark",
		"note": "The collection for the question_banks",
		"hidden": False,
		"singleton": False,
		"translations": [
			{
				"language": "en-US",
				"translation": "question_bank"
			}
		],
	},
	"schema": {
		"name": "lms_question_bank",
		"comment": None
	},
	"fields": [
    {
      "field": "id",
      "type": "uuid",
      "meta": {
        "icon": "id",
        "readonly": True,
        "hidden": True
      },
      "schema": {
        "is_primary_key": True,
        "is_nullable": False
      }
    }
	]
}

lms_question_bank_fields = [
    {
        "collection": "lms_question_bank",
        "field": "status",
        "type": "string",
        "meta": {
            "collection": "lms_question_bank",
            "field": "status",
            "interface": "select-dropdown",
            "options": {"choices": ["draft", "published", "archived"]},
            "required": True,
            "default_value": "draft",
            "sort": 2,
            "width": "half-space",
            "note": "Status of the question"
        },
        "schema": {
            "name": "status",
            "table": "lms_question_bank",
            "data_type": "varchar",
            "max_length": 255,
            "is_nullable": False
        }
    },
    {
        "collection": "lms_question_bank",
        "field": "sort",
        "type": "integer",
        "meta": {
            "collection": "lms_question_bank",
            "field": "sort",
            "interface": "input",
            "sort": 3,
            "width": "half",
            "hidden": True,
            "note": "Sorting order of the question"
        },
        "schema": {
            "name": "sort",
            "table": "lms_question_bank",
            "data_type": "integer",
            "is_nullable": True
        }
    },
    {
        "collection": "lms_question_bank",
        "field": "date_created",
        "type": "timestamp",
        "meta": {
            "collection": "lms_question_bank",
            "field": "date_created",
            "interface": "datetime",
            "readonly": True,
            "hidden": True,
            "sort": 4,
            "width": "half",
            "note": "The date when the question was created"
        },
        "schema": {
            "name": "date_created",
            "table": "lms_question_bank",
            "data_type": "timestamp with time zone",
            "is_nullable": True
        }
    },
    {
        "collection": "lms_question_bank",
        "field": "date_updated",
        "type": "timestamp",
        "meta": {
            "collection": "lms_question_bank",
            "field": "date_updated",
            "interface": "datetime",
            "readonly": True,
            "hidden": True,
            "sort": 5,
            "width": "half",
            "note": "The date when the question was last updated"
        },
        "schema": {
            "name": "date_updated",
            "table": "lms_question_bank",
            "data_type": "timestamp with time zone",
            "is_nullable": True
        }
    },
    {
        "collection": "lms_question_bank",
        "field": "question_text",
        "type": "string",
        "meta": {
            "collection": "lms_question_bank",
            "field": "question_text",
            "interface": "input",
            "sort": 6,
            "width": "full",
            "note": "Text of the question",
            "required": True
        },
        "schema": {
            "name": "question_text",
            "table": "lms_question_bank",
            "data_type": "varchar",
            "max_length": 255,
            "is_nullable": True
        }
    },
    {
        "collection": "lms_question_bank",
        "field": "question_type",
        "type": "string",
        "meta": {
            "collection": "lms_question_bank",
            "field": "question_type",
            "interface": "select-dropdown",
            "options": {"choices": ["true_false", "multiple_choice", "open_ended"]},
            "sort": 7,
            "width": "half",
            "note": "Type of the question",
            "required": True
        },
        "schema": {
            "name": "question_type",
            "table": "lms_question_bank",
            "data_type": "varchar",
            "max_length": 255,
            "is_nullable": True
        }
    },
    {
        "collection": "lms_question_bank",
        "field": "true_false_answer",
        "type": "string",
        "meta": {
            "collection": "lms_question_bank",
            "field": "true_false_answer",
            "interface": "select-dropdown",
            "options": {"choices": ["true", "false"]},
            "sort": 8,
            "width": "half",
            "note": "Answer for true/false questions"
        },
        "schema": {
            "name": "true_false_answer",
            "table": "lms_question_bank",
            "data_type": "varchar",
            "max_length": 255,
            "is_nullable": True
        }
    },
    {
        "collection": "lms_question_bank",
        "field": "multiple_choice_answers",
        "type": "json",
        "meta": {
            "collection": "lms_question_bank",
            "field": "multiple_choice_answers",
            "interface": "json",
            "sort": 9,
            "width": "full",
            "note": "JSON array of multiple choice answers"
        },
        "schema": {
            "name": "multiple_choice_answers",
            "table": "lms_question_bank",
            "data_type": "json",
            "is_nullable": True
        }
    },
    {
        "collection": "lms_question_bank",
        "field": "open_correct_answer",
        "type": "string",
        "meta": {
            "collection": "lms_question_bank",
            "field": "open_correct_answer",
            "interface": "input",
            "sort": 10,
            "width": "full",
            "note": "Correct answer for open-ended questions"
        },
        "schema": {
            "name": "open_correct_answer",
            "table": "lms_question_bank",
            "data_type": "varchar",
            "max_length": 255,
            "is_nullable": True
        }
    },
    {
        "collection": "lms_question_bank",
        "field": "explanation",
        "type": "text",
        "meta": {
            "collection": "lms_question_bank",
            "field": "explanation",
            "interface": "textarea",
            "sort": 11,
            "width": "full",
            "note": "Explanation for the correct answer"
        },
        "schema": {
            "name": "explanation",
            "table": "lms_question_bank",
            "data_type": "text",
            "is_nullable": True
        }
    }
]