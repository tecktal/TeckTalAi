
lms_lessons_resources = {
	"collection": "lms_lessons_resources",
	"meta": {
		"collection": "lms_lessons_resources",
        "group": "lms_content",
		"icon": "",
		"note": "The collection for the lessons_resourcess",
		"hidden": False,
		"singleton": False,
		"translations": [
			{
				"language": "en-US",
				"translation": "lessons_resources"
			}
		],
	},
	"schema": {
		"name": "lms_lessons_resources",
		"comment": None
	},
	"fields": [
		    {
      "field": "id",
      "type": "uuid",
      "meta": {
        "icon": "id",
        "readonly": True,  # Make it read-only to prevent editing
        "hidden": True      # Hide it in the Data Studio UI
      },
      "schema": {
        "is_primary_key": True,
        "is_nullable": False
      }
    }
	]
}

lms_lessons_ressources_fields = [
    {
        "collection": "lms_lessons_resources",
        "field": "status",
        "type": "string",
        "meta": {
            "collection": "lms_lessons_resources",
            "field": "status",
            "interface": "select-dropdown",
            "options": {"choices": ["draft", "published", "archived"]},
            "required": True,
            "default_value": "draft",
            "sort": 1,
            "width": "half-space",
            "note": "Status of the lesson resource"
        },
        "schema": {
            "name": "status",
            "table": "lms_lessons_resources",
            "data_type": "varchar",
            "max_length": 255,
            "is_nullable": False
        }
    },
    {
        "collection": "lms_lessons_resources",
        "field": "sort",
        "type": "integer",
        "meta": {
            "collection": "lms_lessons_resources",
            "field": "sort",
            "interface": "input",
            "sort": 2,
            "width": "half",
            "hidden": True,
            "note": "Sorting order of the lesson resource"
        },
        "schema": {
            "name": "sort",
            "table": "lms_lessons_resources",
            "data_type": "integer",
            "is_nullable": True
        }
    },
    {
        "collection": "lms_lessons_resources",
        "field": "date_created",
        "type": "timestamp",
        "meta": {
            "collection": "lms_lessons_resources",
            "field": "date_created",
            "interface": "datetime",
            "readonly": True,
            "hidden": True,
            "sort": 3,
            "width": "half",
            "note": "The date when the lesson resource was created"
        },
        "schema": {
            "name": "date_created",
            "table": "lms_lessons_resources",
            "data_type": "timestamp with time zone",
            "is_nullable": True
        }
    },
    {
        "collection": "lms_lessons_resources",
        "field": "date_updated",
        "type": "timestamp",
        "meta": {
            "collection": "lms_lessons_resources",
            "field": "date_updated",
            "interface": "datetime",
            "readonly": True,
            "hidden": True,
            "sort": 4,
            "width": "half",
            "note": "The date when the lesson resource was last updated"
        },
        "schema": {
            "name": "date_updated",
            "table": "lms_lessons_resources",
            "data_type": "timestamp with time zone",
            "is_nullable": True
        }
    },
    {
        "collection": "lms_lessons_resources",
        "field": "ressource_type",
        "type": "string",
        "meta": {
            "collection": "lms_lessons_resources",
            "field": "ressource_type",
            "interface": "select-dropdown",
            "options": {
                "choices": [
                    {"text": "URL", "value": "url"},
                    {"text": "File", "value": "file"},
                    {"text": "External Link", "value": "external"}
                ]
            },
            "sort": 5,
            "width": "half",
            "note": "Type of lesson resource"
        },
        "schema": {
            "name": "ressource_type",
            "table": "lms_lessons_resources",
            "data_type": "varchar",
            "max_length": 255,
            "is_nullable": True
        }
    },
    {
        "collection": "lms_lessons_resources",
        "field": "url",
        "type": "string",
        "meta": {
            "collection": "lms_lessons_resources",
            "field": "url",
            "interface": "input",
            "sort": 6,
            "width": "full",
            "note": "URL for the lesson resource"
        },
        "schema": {
            "name": "url",
            "table": "lms_lessons_resources",
            "data_type": "varchar",
            "max_length": 255,
            "is_nullable": True
        }
    },
    {
        "collection": "lms_lessons_resources",
        "field": "title",
        "type": "string",
        "meta": {
            "collection": "lms_lessons_resources",
            "field": "title",
            "interface": "input",
            "sort": 7,
            "width": "full",
            "note": "Title of the lesson resource",
            "required": True
        },
        "schema": {
            "name": "title",
            "table": "lms_lessons_resources",
            "data_type": "varchar",
            "max_length": 255,
            "is_nullable": True
        }
    },
    {
        "collection": "lms_lessons_resources",
        "field": "description",
        "type": "text",
        "meta": {
            "collection": "lms_lessons_resources",
            "field": "description",
            "interface": "wysiwyg",
            "sort": 8,
            "width": "full",
            "note": "Description of the lesson resource"
        },
        "schema": {
            "name": "description",
            "table": "lms_lessons_resources",
            "data_type": "text",
            "is_nullable": True
        }
    }
]