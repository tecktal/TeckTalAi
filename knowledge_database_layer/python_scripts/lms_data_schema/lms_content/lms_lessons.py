
lms_lesson = {
	"collection": "lms_lesson",
	"meta": {
		"collection": "lms_lesson",
        "group": "lms_content",
		"icon": "video_library",
		"note": "The collection for the lessons",
		"hidden": False,
		"singleton": False,
		"translations": [
			{
				"language": "en-US",
				"translation": "lesson"
			}
		],
	},
	"schema": {
		"name": "lms_lesson",
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

lms_lessons_fields = [
    {
        "collection": "lms_lesson",
        "field": "status",
        "type": "string",
        "meta": {
            "collection": "lms_lesson",
            "field": "status",
            "interface": "select-dropdown",
            "options": {"choices": ["draft", "published", "archived"]},
            "required": True,
            "default_value": "draft",
            "sort": 1,
            "width": "half-space",
            "note": "Status of the lesson"
        },
        "schema": {
            "name": "status",
            "table": "lms_lesson",
            "data_type": "varchar",
            "max_length": 255,
            "is_nullable": False
        }
    },
    {
        "collection": "lms_lesson",
        "field": "sort",
        "type": "integer",
        "meta": {
            "collection": "lms_lesson",
            "field": "sort",
            "interface": "input",
            "sort": 2,
            "width": "half",
            "hidden": True,
            "note": "Sorting order of the lesson"
        },
        "schema": {
            "name": "sort",
            "table": "lms_lesson",
            "data_type": "integer",
            "is_nullable": True
        }
    },
    {
        "collection": "lms_lesson",
        "field": "date_created",
        "type": "timestamp",
        "meta": {
            "collection": "lms_lesson",
            "field": "date_created",
            "interface": "datetime",
            "readonly": True,
            "hidden": True,
            "sort": 3,
            "width": "half",
            "note": "The date when the lesson was created"
        },
        "schema": {
            "name": "date_created",
            "table": "lms_lesson",
            "data_type": "timestamp with time zone",
            "is_nullable": True
        }
    },
    {
        "collection": "lms_lesson",
        "field": "date_updated",
        "type": "timestamp",
        "meta": {
            "collection": "lms_lesson",
            "field": "date_updated",
            "interface": "datetime",
            "readonly": True,
            "hidden": True,
            "sort": 4,
            "width": "half",
            "note": "The date when the lesson was last updated"
        },
        "schema": {
            "name": "date_updated",
            "table": "lms_lesson",
            "data_type": "timestamp with time zone",
            "is_nullable": True
        }
    },
    {
        "collection": "lms_lesson",
        "field": "title",
        "type": "string",
        "meta": {
            "collection": "lms_lesson",
            "field": "title",
            "interface": "input",
            "sort": 5,
            "width": "full",
            "note": "Title of the lesson",
            "required": True
        },
        "schema": {
            "name": "title",
            "table": "lms_lesson",
            "data_type": "varchar",
            "max_length": 255,
            "is_nullable": True
        }
    },
    {
        "collection": "lms_lesson",
        "field": "slug",
        "type": "string",
        "meta": {
            "collection": "lms_lesson",
            "field": "slug",
            "interface": "input",
            "sort": 6,
            "width": "full",
            "note": "URL-friendly identifier for the lesson",
            "required": True
        },
        "schema": {
            "name": "slug",
            "table": "lms_lesson",
            "data_type": "varchar",
            "max_length": 255,
            "is_nullable": True
        }
    },
    {
        "collection": "lms_lesson",
        "field": "date_published",
        "type": "timestamp",
        "meta": {
            "collection": "lms_lesson",
            "field": "date_published",
            "interface": "datetime",
            "sort": 7,
            "width": "half",
            "note": "Date when the lesson was published"
        },
        "schema": {
            "name": "date_published",
            "table": "lms_lesson",
            "data_type": "timestamp",
            "is_nullable": True
        }
    },
    {
        "collection": "lms_lesson",
        "field": "video_type",
        "type": "string",
        "meta": {
            "collection": "lms_lesson",
            "field": "video_type",
            "interface": "select-dropdown",
            "options": {
                "choices": [
                    {"text": "Upload", "value": "upload"},
                    {"text": "External URL", "value": "url"}
                ]
            },
            "sort": 8,
            "width": "half",
            "note": "Type of video content"
        },
        "schema": {
            "name": "video_type",
            "table": "lms_lesson",
            "data_type": "varchar",
            "max_length": 255,
            "is_nullable": True
        }
    },
    {
        "collection": "lms_lesson",
        "field": "video_url",
        "type": "string",
        "meta": {
            "collection": "lms_lesson",
            "field": "video_url",
            "interface": "input",
            "sort": 9,
            "width": "full",
            "note": "URL for external video content"
        },
        "schema": {
            "name": "video_url",
            "table": "lms_lesson",
            "data_type": "varchar",
            "max_length": 255,
            "is_nullable": True
        }
    },
    {
        "collection": "lms_lesson",
        "field": "video_duration",
        "type": "string",
        "meta": {
            "collection": "lms_lesson",
            "field": "video_duration",
            "interface": "input",
            "sort": 10,
            "width": "half",
            "note": "Duration of the video lesson"
        },
        "schema": {
            "name": "video_duration",
            "table": "lms_lesson",
            "data_type": "varchar",
            "max_length": 255,
            "is_nullable": True
        }
    },
    {
        "collection": "lms_lesson",
        "field": "video_chapters",
        "type": "json",
        "meta": {
            "collection": "lms_lesson",
            "field": "video_chapters",
            "interface": "repeater",
            "sort": 11,
            "width": "full",
            "note": "Chapters or segments of the video lesson"
        },
        "schema": {
            "name": "video_chapters",
            "table": "lms_lesson",
            "data_type": "json",
            "is_nullable": True
        }
    },
    {
        "collection": "lms_lesson",
        "field": "video_transcript",
        "type": "text",
        "meta": {
            "collection": "lms_lesson",
            "field": "video_transcript",
            "interface": "textarea",
            "sort": 12,
            "width": "full",
            "note": "Transcript of the video lesson"
        },
        "schema": {
            "name": "video_transcript",
            "table": "lms_lesson",
            "data_type": "text",
            "is_nullable": True
        }
    },
    {
        "collection": "lms_lesson",
        "field": "content",
        "type": "text",
        "meta": {
            "collection": "lms_lesson",
            "field": "content",
            "interface": "wysiwyg",
            "sort": 13,
            "width": "full",
            "note": "Additional content or lesson notes"
        },
        "schema": {
            "name": "content",
            "table": "lms_lesson",
            "data_type": "text",
            "is_nullable": True
        }
    }
]