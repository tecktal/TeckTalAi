
lms_enrollement = {
	"collection": "lms_enrollement",
	"meta": {
		"collection": "lms_enrollement",
        "group": "lms_data",
		"icon": "library_add_check",
		"note": "The collection for the enrollements",
		"hidden": False,
		"singleton": False,
		"translations": [
			{
				"language": "en-US",
				"translation": "enrollement"
			}
		],
	},
	"schema": {
		"name": "lms_enrollement",
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

lms_enrollments_fields = [
    {
        "collection": "lms_enrollement",
        "field": "status",
        "type": "string",
        "meta": {
            "collection": "lms_enrollement",
            "field": "status",
            "interface": "select-dropdown",
            "options": {"choices": ["draft", "published", "archived"]},
            "required": True,
            "default_value": "draft",
            "sort": 2,
            "width": "half-space",
            "note": "Status of the enrollment"
        },
        "schema": {
            "name": "status",
            "table": "lms_enrollement",
            "data_type": "varchar",
            "max_length": 255,
            "is_nullable": False
        }
    },
    {
        "collection": "lms_enrollement",
        "field": "sort",
        "type": "integer",
        "meta": {
            "collection": "lms_enrollement",
            "field": "sort",
            "interface": "input",
            "sort": 3,
            "width": "half",
            "hidden": True,
            "note": "Sorting order of the enrollment"
        },
        "schema": {
            "name": "sort",
            "table": "lms_enrollement",
            "data_type": "integer",
            "is_nullable": True
        }
    },
    {
        "collection": "lms_enrollement",
        "field": "date_created",
        "type": "timestamp",
        "meta": {
            "collection": "lms_enrollement",
            "field": "date_created",
            "interface": "datetime",
            "readonly": True,
            "hidden": True,
            "sort": 4,
            "width": "half",
            "note": "The date when the enrollment was created"
        },
        "schema": {
            "name": "date_created",
            "table": "lms_enrollement",
            "data_type": "timestamp with time zone",
            "is_nullable": True
        }
    },
    {
        "collection": "lms_enrollement",
        "field": "date_updated",
        "type": "timestamp",
        "meta": {
            "collection": "lms_enrollement",
            "field": "date_updated",
            "interface": "datetime",
            "readonly": True,
            "hidden": True,
            "sort": 5,
            "width": "half",
            "note": "The date when the enrollment was last updated"
        },
        "schema": {
            "name": "date_updated",
            "table": "lms_enrollement",
            "data_type": "timestamp with time zone",
            "is_nullable": True
        }
    },
    {
        "collection": "lms_enrollement",
        "field": "is_completed",
        "type": "boolean",
        "meta": {
            "collection": "lms_enrollement",
            "field": "is_completed",
            "interface": "boolean",
            "sort": 6,
            "width": "half",
            "note": "Indicates if the enrollment is completed"
        },
        "schema": {
            "name": "is_completed",
            "table": "lms_enrollement",
            "data_type": "boolean",
            "is_nullable": True
        }
    },
    {
        "collection": "lms_enrollement",
        "field": "date_completed",
        "type": "timestamp",
        "meta": {
            "collection": "lms_enrollement",
            "field": "date_completed",
            "interface": "datetime",
            "sort": 7,
            "width": "half",
            "note": "Date when the enrollment was completed"
        },
        "schema": {
            "name": "date_completed",
            "table": "lms_enrollement",
            "data_type": "timestamp",
            "is_nullable": True
        }
    },
    {
        "collection": "lms_enrollement",
        "field": "percent_complete",
        "type": "string",
        "meta": {
            "collection": "lms_enrollement",
            "field": "percent_complete",
            "interface": "input",
            "sort": 8,
            "width": "half",
            "note": "Percentage of course completion"
        },
        "schema": {
            "name": "percent_complete",
            "table": "lms_enrollement",
            "data_type": "varchar",
            "max_length": 255,
            "is_nullable": True
        }
    }
]