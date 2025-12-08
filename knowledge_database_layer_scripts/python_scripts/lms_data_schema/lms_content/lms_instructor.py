
lms_instructor = {
	"collection": "lms_instructor",
	"meta": {
		"collection": "lms_instructor",
        "group": "lms_content",
		"icon": "person",
		"note": "The collection for the instructors",
		"hidden": False,
		"singleton": False,
		"translations": [
			{
				"language": "en-US",
				"translation": "instructor"
			}
		],
	},
	"schema": {
		"name": "lms_instructor",
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

lms_instructors_fields = [
    {
        "collection": "lms_instructor",
        "field": "status",
        "type": "string",
        "meta": {
            "collection": "lms_instructor",
            "field": "status",
            "interface": "select-dropdown",
            "options": {"choices": ["draft", "published", "archived"]},
            "required": True,
            "default_value": "draft",
            "sort": 1,
            "width": "half-space",
            "note": "Status of the instructor profile"
        },
        "schema": {
            "name": "status",
            "table": "lms_instructor",
            "data_type": "varchar",
            "max_length": 255,
            "is_nullable": False
        }
    },
    {
        "collection": "lms_instructor",
        "field": "sort",
        "type": "integer",
        "meta": {
            "collection": "lms_instructor",
            "field": "sort",
            "interface": "input",
            "sort": 2,
            "width": "half",
            "hidden": True,
            "note": "Sorting order of the instructor"
        },
        "schema": {
            "name": "sort",
            "table": "lms_instructor",
            "data_type": "integer",
            "is_nullable": True
        }
    },
    {
        "collection": "lms_instructor",
        "field": "date_created",
        "type": "timestamp",
        "meta": {
            "collection": "lms_instructor",
            "field": "date_created",
            "interface": "datetime",
            "readonly": True,
            "hidden": True,
            "sort": 3,
            "width": "half",
            "note": "The date when the instructor profile was created"
        },
        "schema": {
            "name": "date_created",
            "table": "lms_instructor",
            "data_type": "timestamp with time zone",
            "is_nullable": True
        }
    },
    {
        "collection": "lms_instructor",
        "field": "date_updated",
        "type": "timestamp",
        "meta": {
            "collection": "lms_instructor",
            "field": "date_updated",
            "interface": "datetime",
            "readonly": True,
            "hidden": True,
            "sort": 4,
            "width": "half",
            "note": "The date when the instructor profile was last updated"
        },
        "schema": {
            "name": "date_updated",
            "table": "lms_instructor",
            "data_type": "timestamp with time zone",
            "is_nullable": True
        }
    },
    {
        "collection": "lms_instructor",
        "field": "first_name",
        "type": "string",
        "meta": {
            "collection": "lms_instructor",
            "field": "first_name",
            "interface": "input",
            "sort": 5,
            "width": "half",
            "note": "First name of the instructor",
            "required": True
        },
        "schema": {
            "name": "first_name",
            "table": "lms_instructor",
            "data_type": "varchar",
            "max_length": 255,
            "is_nullable": True
        }
    },
    {
        "collection": "lms_instructor",
        "field": "last_name",
        "type": "string",
        "meta": {
            "collection": "lms_instructor",
            "field": "last_name",
            "interface": "input",
            "sort": 6,
            "width": "half",
            "note": "Last name of the instructor",
            "required": True
        },
        "schema": {
            "name": "last_name",
            "table": "lms_instructor",
            "data_type": "varchar",
            "max_length": 255,
            "is_nullable": True
        }
    },
    {
        "collection": "lms_instructor",
        "field": "slug",
        "type": "string",
        "meta": {
            "collection": "lms_instructor",
            "field": "slug",
            "interface": "input",
            "sort": 7,
            "width": "full",
            "note": "URL-friendly identifier for the instructor",
            "required": True
        },
        "schema": {
            "name": "slug",
            "table": "lms_instructor",
            "data_type": "varchar",
            "max_length": 255,
            "is_nullable": True
        }
    },
    {
        "collection": "lms_instructor",
        "field": "title",
        "type": "string",
        "meta": {
            "collection": "lms_instructor",
            "field": "title",
            "interface": "input",
            "sort": 8,
            "width": "full",
            "note": "Professional title of the instructor"
        },
        "schema": {
            "name": "title",
            "table": "lms_instructor",
            "data_type": "varchar",
            "max_length": 255,
            "is_nullable": True
        }
    },
    {
        "collection": "lms_instructor",
        "field": "bio",
        "type": "text",
        "meta": {
            "collection": "lms_instructor",
            "field": "bio",
            "interface": "wysiwyg",
            "sort": 9,
            "width": "full",
            "note": "Biographical information about the instructor"
        },
        "schema": {
            "name": "bio",
            "table": "lms_instructor",
            "data_type": "text",
            "is_nullable": True
        }
    },
    {
        "collection": "lms_instructor",
        "field": "links",
        "type": "json",
        "meta": {
            "collection": "lms_instructor",
            "field": "links",
            "interface": "repeater",
            "sort": 10,
            "width": "full",
            "note": "Professional or social media links for the instructor"
        },
        "schema": {
            "name": "links",
            "table": "lms_instructor",
            "data_type": "json",
            "is_nullable": True
        }
    }
]