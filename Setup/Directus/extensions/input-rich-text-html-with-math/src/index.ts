import { defineInterface } from '@directus/extensions-sdk';
import InterfaceComponent from './interface.vue';

export default defineInterface({
	id: 'input-rich-text-html-with-math',
	name: 'Rich Text with Math',
	description: 'WYSIWYG editor with MathJax support for LaTeX mathematical expressions',
	icon: 'functions',
	component: InterfaceComponent,
	types: ['text'],
	group: 'standard',
	options: {
		standard: [
			{
				field: 'toolbar',
				name: 'Toolbar',
				type: 'json',
				schema: {
					default_value: ['bold', 'italic', 'underline', 'strikethrough', '|', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', '|', 'alignleft', 'aligncenter', 'alignright', 'alignjustify', '|', 'bullist', 'numlist', '|', 'link', 'image', 'media', '|', 'math', 'rendermath'],
				},
				meta: {
					width: 'half',
					interface: 'select-multiple-dropdown',
					options: {
						choices: [
							{
								value: 'undo',
								text: 'Undo',
							},
							{
								value: 'redo',
								text: 'Redo',
							},
							{
								value: 'bold',
								text: 'Bold',
							},
							{
								value: 'italic',
								text: 'Italic',
							},
							{
								value: 'underline',
								text: 'Underline',
							},
							{
								value: 'strikethrough',
								text: 'Strikethrough',
							},
							{
								value: 'subscript',
								text: 'Subscript',
							},
							{
								value: 'superscript',
								text: 'Superscript',
							},
							{
								value: 'fontfamily',
								text: 'Font Family',
							},
							{
								value: 'fontsize',
								text: 'Font Size',
							},
							{
								value: 'h1',
								text: 'Heading 1',
							},
							{
								value: 'h2',
								text: 'Heading 2',
							},
							{
								value: 'h3',
								text: 'Heading 3',
							},
							{
								value: 'h4',
								text: 'Heading 4',
							},
							{
								value: 'h5',
								text: 'Heading 5',
							},
							{
								value: 'h6',
								text: 'Heading 6',
							},
							{
								value: 'alignleft',
								text: 'Align Left',
							},
							{
								value: 'aligncenter',
								text: 'Align Center',
							},
							{
								value: 'alignright',
								text: 'Align Right',
							},
							{
								value: 'alignjustify',
								text: 'Justify',
							},
							{
								value: 'indent',
								text: 'Increase Indent',
							},
							{
								value: 'outdent',
								text: 'Decrease Indent',
							},
							{
								value: 'numlist',
								text: 'Numbered List',
							},
							{
								value: 'bullist',
								text: 'Bullet List',
							},
							{
								value: 'forecolor',
								text: 'Text Color',
							},
							{
								value: 'backcolor',
								text: 'Background Color',
							},
							{
								value: 'removeformat',
								text: 'Clear Formatting',
							},
							{
								value: 'link',
								text: 'Link',
							},
							{
								value: 'unlink',
								text: 'Unlink',
							},
							{
								value: 'image',
								text: 'Image',
							},
							{
								value: 'media',
								text: 'Media',
							},
							{
								value: 'table',
								text: 'Table',
							},
							{
								value: 'hr',
								text: 'Horizontal Line',
							},
							{
								value: 'fullscreen',
								text: 'Fullscreen',
							},
							{
								value: 'code',
								text: 'Source Code',
							},
							{
								value: 'math',
								text: 'Insert Math (∑)',
							},
							{
								value: 'rendermath',
								text: 'Render Math (🔄)',
							},
						],
					},
				},
			},
			{
				field: 'font',
				name: 'Font Family',
				type: 'string',
				meta: {
					width: 'half',
					interface: 'select-dropdown',
					options: {
						choices: [
							{ text: 'Sans Serif', value: 'sans-serif' },
							{ text: 'Serif', value: 'serif' },
							{ text: 'Monospace', value: 'monospace' },
						],
					},
				},
				schema: {
					default_value: 'sans-serif',
				},
			},
			{
				field: 'direction',
				name: 'Text Direction',
				type: 'string',
				meta: {
					width: 'half',
					interface: 'select-dropdown',
					options: {
						choices: [
							{ text: 'Left to Right', value: 'ltr' },
							{ text: 'Right to Left', value: 'rtl' },
						],
					},
				},
				schema: {
					default_value: 'ltr',
				},
			},
		],
		advanced: [
			{
				field: 'softLength',
				name: 'Character Limit',
				type: 'integer',
				meta: {
					width: 'half',
					interface: 'input',
					options: {
						placeholder: '255',
						min: 1,
					},
				},
			},
			{
				field: 'customFormats',
				name: 'Custom Formats',
				type: 'json',
				meta: {
					interface: 'input-code',
					note: 'Define custom text formats with styles and attributes',
					options: {
						language: 'json',
						template: JSON.stringify(
							[
								{
									title: 'My Custom Format',
									inline: 'span',
									classes: 'custom-wrapper',
									styles: { color: '#00ff00', 'font-size': '20px' },
									attributes: { title: 'My Custom Wrapper' },
								},
							],
							null,
							4,
						),
					},
				},
			},
			{
				field: 'tinymceOverrides',
				name: 'TinyMCE Overrides',
				type: 'json',
				meta: {
					interface: 'input-code',
					note: 'Override TinyMCE configuration options',
					options: {
						language: 'json',
						template: JSON.stringify(
							{
								font_size_formats: '8pt 10pt 12pt 14pt 16pt 18pt 24pt 36pt 48pt',
								font_family_formats: 'Arial=arial,helvetica,sans-serif; Courier New=courier new,courier,monospace;',
							},
							null,
							4,
						),
					},
				},
			},
		],
	},
});
