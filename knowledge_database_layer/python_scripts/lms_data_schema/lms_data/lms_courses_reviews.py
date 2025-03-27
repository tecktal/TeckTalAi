
lms_courses_reviews = {
	"collection": "lms_courses_reviews",
	"meta": {
		"collection": "lms_courses_reviews",
        "group": "lms_data",
		"icon": "star_half",
		"note": "The collection for the courses_reviewss",
		"hidden": False,
		"singleton": False,
		"translations": [
			{
				"language": "en-US",
				"translation": "courses_reviews"
			}
		],
	},
	"schema": {
		"name": "lms_courses_reviews",
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
lms_course_reviews_fields = [
    {
        "collection": "lms_courses_reviews",
        "field": "status",
        "type": "string",
        "meta": {
            "collection": "lms_courses_reviews",
            "field": "status",
            "interface": "select-dropdown",
            "options": {"choices": ["draft", "published", "archived"]},
            "required": True,
            "default_value": "draft",
            "sort": 2,
            "width": "half-space",
            "note": "Status of the course review"
        },
        "schema": {
            "name": "status",
            "table": "lms_courses_reviews",
            "data_type": "varchar",
            "max_length": 255,
            "is_nullable": False
        }
    },
    {
        "collection": "lms_courses_reviews",
        "field": "sort",
        "type": "integer",
        "meta": {
            "collection": "lms_courses_reviews",
            "field": "sort",
            "interface": "input",
            "sort": 3,
            "width": "half",
            "hidden": True,
            "note": "Sorting order of the course review"
        },
        "schema": {
            "name": "sort",
            "table": "lms_courses_reviews",
            "data_type": "integer",
            "is_nullable": True
        }
    },
    {
        "collection": "lms_courses_reviews",
        "field": "date_created",
        "type": "timestamp",
        "meta": {
            "collection": "lms_courses_reviews",
            "field": "date_created",
            "interface": "datetime",
            "readonly": True,
            "hidden": True,
            "sort": 4,
            "width": "half",
            "note": "The date when the course review was created"
        },
        "schema": {
            "name": "date_created",
            "table": "lms_courses_reviews",
            "data_type": "timestamp with time zone",
            "is_nullable": True
        }
    },
    {
        "collection": "lms_courses_reviews",
        "field": "date_updated",
        "type": "timestamp",
        "meta": {
            "collection": "lms_courses_reviews",
            "field": "date_updated",
            "interface": "datetime",
            "readonly": True,
            "hidden": True,
            "sort": 5,
            "width": "half",
            "note": "The date when the course review was last updated"
        },
        "schema": {
            "name": "date_updated",
            "table": "lms_courses_reviews",
            "data_type": "timestamp with time zone",
            "is_nullable": True
        }
    },
    {
        "collection": "lms_courses_reviews",
        "field": "rating",
        "type": "integer",
        "meta": {
            "collection": "lms_courses_reviews",
            "field": "rating",
            "interface": "rating",
            "sort": 6,
            "width": "half",
            "note": "Rating for the course",
            "required": True
        },
        "schema": {
            "name": "rating",
            "table": "lms_courses_reviews",
            "data_type": "integer",
            "is_nullable": True
        }
    },
    {
        "collection": "lms_courses_reviews",
        "field": "message",
        "type": "text",
        "meta": {
            "collection": "lms_courses_reviews",
            "field": "message",
            "interface": "textarea",
            "sort": 7,
            "width": "full",
            "note": "Review message from the user"
        },
        "schema": {
            "name": "message",
            "table": "lms_courses_reviews",
            "data_type": "text",
            "is_nullable": True
        }
    },
    {
        "collection": "lms_courses_reviews",
        "field": "instructor_response",
        "type": "text",
        "meta": {
            "collection": "lms_courses_reviews",
            "field": "instructor_response",
            "interface": "textarea",
            "sort": 8,
            "width": "full",
            "note": "Response from the course instructor"
        },
        "schema": {
            "name": "instructor_response",
            "table": "lms_courses_reviews",
            "data_type": "text",
            "is_nullable": True
        }
    }
]