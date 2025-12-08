
lms_settings = {
	"collection": "lms_settings",
	"meta": {
		"collection": "lms_settings",
        "group": "lms_metadata",
		"icon": "globe_uk",
		"note": "The collection for the settingss",
		"hidden": False,
		"singleton": False,
		"translations": [
			{
				"language": "en-US",
				"translation": "settings"
			}
		],
	},
	"schema": {
		"name": "lms_settings",
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

lms_settings_fields = [
    {
        "collection": "lms_settings",
        "field": "date_created",
        "type": "timestamp",
        "meta": {
            "collection": "lms_settings",
            "field": "date_created",
            "interface": "datetime",
            "readonly": True,
            "hidden": True,
            "sort": 1,
            "width": "half",
            "note": "The date when the settings were created"
        },
        "schema": {
            "name": "date_created",
            "table": "lms_settings",
            "data_type": "timestamp with time zone",
            "is_nullable": True
        }
    },
    {
        "collection": "lms_settings",
        "field": "date_updated",
        "type": "timestamp",
        "meta": {
            "collection": "lms_settings",
            "field": "date_updated",
            "interface": "datetime",
            "readonly": True,
            "hidden": True,
            "sort": 2,
            "width": "half",
            "note": "The date when the settings were last updated"
        },
        "schema": {
            "name": "date_updated",
            "table": "lms_settings",
            "data_type": "timestamp with time zone",
            "is_nullable": True
        }
    },
    {
        "collection": "lms_settings",
        "field": "title",
        "type": "string",
        "meta": {
            "collection": "lms_settings",
            "field": "title",
            "interface": "input",
            "sort": 3,
            "width": "full",
            "note": "Title of the LMS",
            "required": True
        },
        "schema": {
            "name": "title",
            "table": "lms_settings",
            "data_type": "varchar",
            "max_length": 255,
            "is_nullable": True
        }
    },
    {
        "collection": "lms_settings",
        "field": "tagline",
        "type": "string",
        "meta": {
            "collection": "lms_settings",
            "field": "tagline",
            "interface": "input",
            "sort": 4,
            "width": "full",
            "note": "Tagline for the LMS"
        },
        "schema": {
            "name": "tagline",
            "table": "lms_settings",
            "data_type": "varchar",
            "max_length": 255,
            "is_nullable": True
        }
    },
    {
        "collection": "lms_settings",
        "field": "description",
        "type": "text",
        "meta": {
            "collection": "lms_settings",
            "field": "description",
            "interface": "textarea",
            "sort": 5,
            "width": "full",
            "note": "Description of the LMS"
        },
        "schema": {
            "name": "description",
            "table": "lms_settings",
            "data_type": "text",
            "is_nullable": True
        }
    },
    {
        "collection": "lms_settings",
        "field": "links",
        "type": "json",
        "meta": {
            "collection": "lms_settings",
            "field": "links",
            "interface": "json",
            "sort": 6,
            "width": "full",
            "note": "JSON object of various links for the LMS"
        },
        "schema": {
            "name": "links",
            "table": "lms_settings",
            "data_type": "json",
            "is_nullable": True
        }
    }
]