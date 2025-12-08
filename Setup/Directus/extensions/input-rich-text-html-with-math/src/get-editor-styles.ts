export default function getEditorStyles(font: 'sans-serif' | 'serif' | 'monospace'): string {
	// Extension-compatible font families
	const fontFamilies = {
		'sans-serif': 'Arial, Helvetica, sans-serif',
		'serif': 'Georgia, serif',
		'monospace': 'Monaco, Menlo, "Ubuntu Mono", monospace'
	};

	const userFontFamily = fontFamilies[font];

	return `
body {
	color: #333;
	background-color: #fff;
	margin: 20px;
	font-family: ${userFontFamily};
	-webkit-font-smoothing: antialiased;
	text-rendering: optimizeLegibility;
	-moz-osx-font-smoothing: grayscale;
}

body.mce-content-readonly {
	color: #666;
	background-color: #f5f5f5;
}

.mce-offscreen-selection {
	display: none;
}

h1, h2, h3, h4, h5, h6 {
	font-family: ${userFontFamily};
	color: #222;
	font-weight: 700;
	margin-block-end: 0;
}

h1 + p, h2 + p, h3 + p, h4 + p, h5 + p, h6 + p {
	margin-block-start: 0.5em;
}

h1 {
	font-size: 36px;
	line-height: 46px;
	margin-block-start: 1em;
}

h2 {
	font-size: 24px;
	line-height: 34px;
	margin-block-start: 1.25em;
}

h3 {
	font-size: 19px;
	line-height: 29px;
	margin-block-start: 1.25em;
}

h4 {
	font-size: 16px;
	line-height: 26px;
	margin-block-start: 1.5em;
}

h5 {
	font-size: 14px;
	line-height: 24px;
	margin-block-start: 2em;
}

h6 {
	font-size: 12px;
	line-height: 22px;
	margin-block-start: 2em;
}

p {
	font-family: ${userFontFamily};
	font-size: 15px;
	line-height: 24px;
	font-weight: 500;
	margin: 1.5em 0;
}

a {
	color: #007cba;
	text-decoration: none;
}

ul, ol {
	font-family: ${userFontFamily};
	font-size: 15px;
	line-height: 24px;
	font-weight: 500;
	margin: 1.5em 0;
}

ul ul,
	ol ol,
		ul ol,
			ol ul {
	margin: 0;
}

b, strong {
	font-weight: 700;
}

code {
	font-size: 15px;
	line-height: 24px;
	font-weight: 500;
	padding: 2px 4px;
	font-family: Monaco, Menlo, "Ubuntu Mono", monospace;
	background-color: #f5f5f5;
	border-radius: 4px;
	overflow-wrap: break-word;
}

pre {
	font-size: 15px;
	line-height: 24px;
	font-weight: 500;
	padding: 1em;
	font-family: Monaco, Menlo, "Ubuntu Mono", monospace;
	background-color: #f5f5f5;
	border-radius: 4px;
	overflow: auto;
}

blockquote {
	font-family: ${userFontFamily};
	font-size: 15px;
	line-height: 24px;
	font-weight: 500;
	border-inline-start: 2px solid #ddd;
	padding-inline-start: 1em;
	margin-inline-start: 0px;
}

video,
img {
	max-inline-size: 100%;
	border-radius: 4px;
	block-size: auto;
}

iframe {
	max-inline-size: 100%;
	border-radius: 4px;
}

hr {
	background-color: #ddd;
	block-size: 1px;
	border: none;
	margin-block-start: 2em;
	margin-block-end: 2em;
}

table {
	border-collapse: collapse;
	font-size: 15px;
	line-height: 24px;
	font-weight: 500;
}

table th,
table td {
	border: 1px solid #ddd;
	padding: 0.4rem;
}

figure {
	display: table;
	margin: 1rem auto;
}

figure figcaption {
	color: #999;
	display: block;
	margin-block-start: 0.25rem;
	text-align: center;
}

/* Math placeholder styles */
.math-tex {
	display: inline-block;
	vertical-align: middle;
	margin: 0 0.12em;
	padding: 0.06em 0.18em;
	border-radius: 4px;
	background: rgba(0,0,0,0.02);
	cursor: pointer;
	user-select: none;
	border: 1px solid transparent;
	transition: all 0.2s ease;
}

.math-tex:hover {
	background: rgba(0,0,0,0.05);
	border-color: rgba(0, 122, 204, 0.3);
}

.math-tex:focus {
	outline: 2px solid rgba(0, 122, 204, 0.25);
	background: rgba(0, 122, 204, 0.05);
}`;
}
