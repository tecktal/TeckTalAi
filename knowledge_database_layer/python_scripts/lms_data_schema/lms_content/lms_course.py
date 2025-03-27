
lms_course = {
	"collection": "lms_course",
	"meta": {
		"collection": "lms_course",
        "group": "lms_content",
		"icon": "collections_bookmark",
		"note": "The collection for the courses",
		"hidden": False,
		"singleton": False,
		"translations": [
			{
				"language": "en-US",
				"translation": "Course"
			}
		],
	},
	"schema": {
		"name": "lms_course",
		"comment": None
	},
	"fields": [    {
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

lms_course_fields = [
    {
        "collection": "lms_course",
        "field": "status",
        "type": "string",
        "meta": {
            "collection": "lms_course",
            "field": "status",
            "interface": "select-dropdown",
            "options": {"choices": ["draft", "published", "archived"]},
            "required": True,
            "default_value": "draft",
            "sort": 2,
            "width": "half-space",
            "note": "Status of the course"
        },
        "schema": {
            "name": "status",
            "table": "lms_course",
            "data_type": "varchar",
            "max_length": 255,
            "is_nullable": False
        }
    },
    {
        "collection": "lms_course",
        "field": "sort",
        "type": "integer",
        "meta": {
            "collection": "lms_course",
            "field": "sort",
            "interface": "input",
            "sort": 3,
            "width": "half",
            "hidden": True ,
            "note": "Sorting order of the course"
        },
        "schema": {
            "name": "sort",
            "table": "lms_course",
            "data_type": "integer",
            "is_nullable": True
        }
    },
    {
        "collection": "lms_course",
        "field": "date_created",
        "type": "timestamp",
        "meta": {
            "collection": "lms_course",
            "field": "date_created",
            "interface": "datetime",
            "readonly": True,
            "hidden":True,
            "sort": 4,
            "width": "half",
            "note": "The date when the course was created"
        },
        "schema": {
            "name": "date_created",
            "table": "lms_course",
            "data_type": "timestamp with time zone",
            "is_nullable": True
        }
    },
    {
        "collection": "lms_course",
        "field": "date_updated",
        "type": "timestamp",
        "meta": {
            "collection": "lms_course",
            "field": "date_updated",
            "interface": "datetime",
            "readonly": True,
            "hidden":True,
            "sort": 5,
            "width": "half",
            "note": "The date when the course was last updated"
        },
        "schema": {
            "name": "date_updated",
            "table": "lms_course",
            "data_type": "timestamp with time zone",
            "is_nullable": True
        }
    },
    {
        "collection": "lms_course",
        "field": "title",
        "type": "string",
        "meta": {
            "collection": "lms_course",
            "field": "title",
            "interface": "input",
            "sort": 6,
            "width": "full",
            "note": "Title of the course",
            "required": True,
        },
        "schema": {
            "name": "title",
            "table": "lms_course",
            "data_type": "varchar",
            "max_length": 255,
            "is_nullable": True
        }
    },
    {
        "collection": "lms_course",
        "field": "slug",
        "type": "string",
        "meta": {
            "collection": "lms_course",
            "field": "slug",
            "interface": "input",
            "sort": 7,
            "width": "half",
            "note": "URL-friendly identifier for the course",
            "required": True,
        },
        "schema": {
            "name": "slug",
            "table": "lms_course",
            "data_type": "varchar",
            "max_length": 255,
            "is_nullable": True
        }
    },
    {
        "collection": "lms_course",
        "field": "date_published",
        "type": "timestamp",
        "meta": {
            "collection": "lms_course",
            "field": "date_published",
            "interface": "datetime",
            "sort": 8,
            "width": "half",
            "note": "Date when the course was published"
        },
        "schema": {
            "name": "date_published",
            "table": "lms_course",
            "data_type": "timestamp",
            "is_nullable": True
        }
    },
    {
        "collection": "lms_course",
        "field": "description",
        "type": "text",
        "meta": {
            "collection": "lms_course",
            "field": "description",
            "interface": "Text",
            "sort": 9,
            "width": "full",
            "note": "Short description of the course"
        },
        "schema": {
            "name": "description",
            "table": "lms_course",
            "data_type": "text",
            "is_nullable": True
        }
    },
    {
        "collection": "lms_course",
        "field": "description_long",
        "type": "text",
        "meta": {
            "collection": "lms_course",
            "field": "description_long",
            "interface": "WYSIWYG",
            "sort": 10,
            "width": "full",
            "note": "Long description of the course"
        },
        "schema": {
            "name": "description_long",
            "table": "lms_course",
            "data_type": "text",
            "is_nullable": True
        }
    }
]
