# Input Rich Text HTML with Math

A Directus extension that provides a rich text editor with MathJax support for LaTeX mathematical expressions.

## Features

- **Rich Text Editing**: Full WYSIWYG editor based on TinyMCE
- **Math Support**: Insert and edit LaTeX mathematical expressions with MathJax rendering
- **Image Management**: Upload and manage images with alt text, dimensions, and lazy loading
- **Media Support**: Handle video, audio, and iframe content
- **Link Management**: Create and edit links with tooltips and target options
- **Source Code Editing**: Edit HTML source code directly
- **Custom Formatting**: Support for custom text formats and styles
- **Responsive Design**: Works on all device sizes
- **Performance Optimized**: Smart content tracking and debounced rendering

## Installation

1. Build the extension:
   ```bash
   npm run build
   ```

2. Copy the `dist` folder to your Directus extensions directory:
   ```
   extensions/interfaces/input-rich-text-html-with-math/
   ```

3. Restart your Directus instance

## Usage

This interface can be used on any text field in your Directus collections. It provides the same functionality as the standard rich text interface but with additional math support.

### Math Features

- **Insert Math**: Click the ∑ button to insert LaTeX expressions
- **Display Math**: Use `$$...$$` for block math or `\(...\)` for inline math
- **Edit Math**: Double-click any math element to edit it
- **Manual Render**: Use the 🔄 button to manually re-render all math

### Toolbar Options

The interface supports all standard TinyMCE toolbar options plus:
- `math`: Insert mathematical expressions
- `rendermath`: Manually render all math

## Configuration

The interface supports several configuration options:

- **Toolbar**: Customize the editor toolbar
- **Font Family**: Choose between sans-serif, serif, or monospace
- **Text Direction**: Support for LTR and RTL text
- **Character Limit**: Set soft character limits with warnings
- **Custom Formats**: Define custom text formats with styles
- **TinyMCE Overrides**: Override any TinyMCE configuration

## Development

To develop this extension:

1. Install dependencies:
   ```bash
   npm install
   ```

2. Start development mode:
   ```bash
   npm run dev
   ```

3. Build for production:
   ```bash
   npm run build
   ```

## Dependencies

- Vue 3
- TinyMCE 6
- MathJax 3
- Lodash

## License

MIT License
