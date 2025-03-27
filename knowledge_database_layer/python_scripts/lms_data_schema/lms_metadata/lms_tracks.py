
lms_tracks = {
	"collection": "lms_tracks",
	"meta": {
		"collection": "lms_tracks",
        "group": "lms_metadata",
		"icon": "conversion_path",
		"note": "The collection for the trackss",
		"hidden": False,
		"singleton": False,
		"translations": [
			{
				"language": "en-US",
				"translation": "tracks"
			}
		],
	},
	"schema": {
		"name": "lms_tracks",
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

lms_track_fields = [
    {
        "collection": "lms_tracks",
        "field": "title",
        "type": "string",
        "meta": {
            "collection": "lms_tracks",
            "field": "title",
            "interface": "input",
            "sort": 1,
            "width": "full",
            "note": "Title of the track",
            "required": True
        },
        "schema": {
            "name": "title",
            "table": "lms_tracks",
            "data_type": "varchar",
            "max_length": 255,
            "is_nullable": True
        }
    },
    {
        "collection": "lms_tracks",
        "field": "slug",
        "type": "string",
        "meta": {
            "collection": "lms_tracks",
            "field": "slug",
            "interface": "input",
            "sort": 2,
            "width": "full",
            "note": "URL-friendly identifier for the track"
        },
        "schema": {
            "name": "slug",
            "table": "lms_tracks",
            "data_type": "varchar",
            "max_length": 255,
            "is_nullable": True
        }
    },
    {
        "collection": "lms_tracks",
        "field": "description",
        "type": "text",
        "meta": {
            "collection": "lms_tracks",
            "field": "description",
            "interface": "text",
            "sort": 3,
            "width": "full",
            "note": "Short description of the track"
        },
        "schema": {
            "name": "description",
            "table": "lms_tracks",
            "data_type": "text",
            "is_nullable": True
        }
    },
    {
        "collection": "lms_tracks",
        "field": "image",
        "type": "uuid",
        "meta": {
            "collection": "lms_tracks",
            "field": "image",
            "interface": "file",
            "sort": 4,
            "width": "half",
            "note": "Cover image for the track"
        },
        "schema": {
            "name": "image",
            "table": "lms_tracks",
            "data_type": "uuid",
            "is_nullable": True,
            "references": {
                "collection": "directus_files",
                "field": "id"
            }
        }
    },
    {
        "collection": "lms_tracks",
        "field": "date_created",
        "type": "timestamp",
        "meta": {
            "collection": "lms_tracks",
            "field": "date_created",
            "interface": "datetime",
            "readonly": True,
            "hidden": True,
            "sort": 5,
            "width": "half",
            "note": "The date when the track was created"
        },
        "schema": {
            "name": "date_created",
            "table": "lms_tracks",
            "data_type": "timestamp with time zone",
            "is_nullable": True
        }
    },
    {
        "collection": "lms_tracks",
        "field": "date_updated",
        "type": "timestamp",
        "meta": {
            "collection": "lms_tracks",
            "field": "date_updated",
            "interface": "datetime",
            "readonly": True,
            "hidden": True,
            "sort": 6,
            "width": "half",
            "note": "The date when the track was last updated"
        },
        "schema": {
            "name": "date_updated",
            "table": "lms_tracks",
            "data_type": "timestamp with time zone",
            "is_nullable": True
        }
    }
]
