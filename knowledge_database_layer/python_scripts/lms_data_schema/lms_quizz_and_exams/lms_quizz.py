
lms_quizz = {
	"collection": "lms_quizz",
	"meta": {
		"collection": "lms_quizz",
        "group": "lms_quizz_and_exams",
		"icon": "assignment",
		"note": "The collection for the quizzs",
		"hidden": False,
		"singleton": False,
		"translations": [
			{
				"language": "en-US",
				"translation": "quizz"
			}
		],
	},
	"schema": {
		"name": "lms_quizz",
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

lms_quizz_fields = [
    {
        "collection": "lms_quizz",
        "field": "status",
        "type": "string",
        "meta": {
            "collection": "lms_quizz",
            "field": "status",
            "interface": "select-dropdown",
            "options": {"choices": ["draft", "published", "archived"]},
            "required": True,
            "default_value": "draft",
            "sort": 2,
            "width": "half-space",
            "note": "Status of the quiz"
        },
        "schema": {
            "name": "status",
            "table": "lms_quizz",
            "data_type": "varchar",
            "max_length": 255,
            "is_nullable": False
        }
    },
    {
        "collection": "lms_quizz",
        "field": "sort",
        "type": "integer",
        "meta": {
            "collection": "lms_quizz",
            "field": "sort",
            "interface": "input",
            "sort": 3,
            "width": "half",
            "hidden": True,
            "note": "Sorting order of the quiz"
        },
        "schema": {
            "name": "sort",
            "table": "lms_quizz",
            "data_type": "integer",
            "is_nullable": True
        }
    },
    {
        "collection": "lms_quizz",
        "field": "date_created",
        "type": "timestamp",
        "meta": {
            "collection": "lms_quizz",
            "field": "date_created",
            "interface": "datetime",
            "readonly": True,
            "hidden": True,
            "sort": 4,
            "width": "half",
            "note": "The date when the quiz was created"
        },
        "schema": {
            "name": "date_created",
            "table": "lms_quizz",
            "data_type": "timestamp with time zone",
            "is_nullable": True
        }
    },
    {
        "collection": "lms_quizz",
        "field": "date_updated",
        "type": "timestamp",
        "meta": {
            "collection": "lms_quizz",
            "field": "date_updated",
            "interface": "datetime",
            "readonly": True,
            "hidden": True,
            "sort": 5,
            "width": "half",
            "note": "The date when the quiz was last updated"
        },
        "schema": {
            "name": "date_updated",
            "table": "lms_quizz",
            "data_type": "timestamp with time zone",
            "is_nullable": True
        }
    },
    {
        "collection": "lms_quizz",
        "field": "title",
        "type": "string",
        "meta": {
            "collection": "lms_quizz",
            "field": "title",
            "interface": "input",
            "sort": 6,
            "width": "full",
            "note": "Title of the quiz",
            "required": True
        },
        "schema": {
            "name": "title",
            "table": "lms_quizz",
            "data_type": "varchar",
            "max_length": 255,
            "is_nullable": True
        }
    },
    {
        "collection": "lms_quizz",
        "field": "description",
        "type": "text",
        "meta": {
            "collection": "lms_quizz",
            "field": "description",
            "interface": "textarea",
            "sort": 7,
            "width": "full",
            "note": "Description of the quiz"
        },
        "schema": {
            "name": "description",
            "table": "lms_quizz",
            "data_type": "text",
            "is_nullable": True
        }
    }
]