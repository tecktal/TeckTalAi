
lms_comments = {
	"collection": "lms_comments",
	"meta": {
		"collection": "lms_comments",
        "group": "lms_data",
		"icon": "mode_comment",
		"note": "The collection for the commentss",
		"hidden": False,
		"singleton": False,
		"translations": [
			{
				"language": "en-US",
				"translation": "comments"
			}
		],
	},
	"schema": {
		"name": "lms_comments",
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
lms_comments_fields = [
    {
        "collection": "lms_comments",
        "field": "sort",
        "type": "integer",
        "meta": {
            "collection": "lms_comments",
            "field": "sort",
            "interface": "input",
            "sort": 1,
            "width": "half",
            "hidden": True,
            "note": "Sorting order of the comment"
        },
        "schema": {
            "name": "sort",
            "table": "lms_comments",
            "data_type": "integer",
            "is_nullable": True
        }
    },
    {
        "collection": "lms_comments",
        "field": "date_created",
        "type": "timestamp",
        "meta": {
            "collection": "lms_comments",
            "field": "date_created",
            "interface": "datetime",
            "readonly": True,
            "hidden": True,
            "sort": 2,
            "width": "half",
            "note": "The date when the comment was created"
        },
        "schema": {
            "name": "date_created",
            "table": "lms_comments",
            "data_type": "timestamp with time zone",
            "is_nullable": True
        }
    },
    {
        "collection": "lms_comments",
        "field": "date_updated",
        "type": "timestamp",
        "meta": {
            "collection": "lms_comments",
            "field": "date_updated",
            "interface": "datetime",
            "readonly": True,
            "hidden": True,
            "sort": 3,
            "width": "half",
            "note": "The date when the comment was last updated"
        },
        "schema": {
            "name": "date_updated",
            "table": "lms_comments",
            "data_type": "timestamp with time zone",
            "is_nullable": True
        }
    },
    {
        "collection": "lms_comments",
        "field": "message",
        "type": "text",
        "meta": {
            "collection": "lms_comments",
            "field": "message",
            "interface": "textarea",
            "sort": 4,
            "width": "full",
            "note": "Comment message",
            "required": True
        },
        "schema": {
            "name": "message",
            "table": "lms_comments",
            "data_type": "text",
            "is_nullable": False
        }
    },
    {
        "collection": "lms_comments",
        "field": "parent_comment",
        "type": "uuid",
        "meta": {
            "collection": "lms_comments",
            "field": "parent_comment",
            "interface": "select-dropdown-m2o",
            "sort": 5,
            "width": "full",
            "note": "Parent comment for nested comments",
            "options": {
                "template": "{{message | truncate(50)}}",
            }
        },
        "schema": {
            "name": "parent_comment",
            "table": "lms_comments",
            "data_type": "uuid",
            "is_nullable": True
        }
    }
]