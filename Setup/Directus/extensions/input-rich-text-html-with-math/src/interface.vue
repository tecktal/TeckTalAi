<template>
	<div :id="field" class="wysiwyg" :class="{ disabled }">
		<editor
			:key="editorKey"
			ref="editorElement"
			v-model="internalValue"
			:init="editorOptions"
			:disabled="editorDisabled"
			model-events="change keydown blur focus paste ExecCommand SetContent"
			@focusin="setFocus(true)"
			@focusout="setFocus(false)"
			@focus="setupContentWatcher"
			@set-content="contentUpdated"
		/>
		<template v-if="softLength">
			<span
				class="remaining"
				:class="{
					warning: percRemaining < 10,
					danger: percRemaining < 5,
				}"
			>
				{{ softLength - count }}
			</span>
		</template>

		<!-- Link Drawer -->
		<div v-if="linkDrawerOpen" class="drawer-overlay" @click="closeLinkDrawer">
			<div class="drawer" @click.stop>
				<div class="drawer-header">
					<h3>Link</h3>
					<button class="close-btn" @click="closeLinkDrawer">×</button>
				</div>
				<div class="drawer-content">
					<div class="field">
						<label>URL</label>
						<input v-model="linkSelection.url" placeholder="Enter URL" class="input" />
					</div>
					<div class="field">
						<label>Display Text</label>
						<input v-model="linkSelection.displayText" placeholder="Enter display text" class="input" />
					</div>
					<div class="field">
						<label>Tooltip</label>
						<input v-model="linkSelection.title" placeholder="Enter tooltip" class="input" />
					</div>
					<div class="field">
						<label>
							<input type="checkbox" v-model="linkSelection.newTab" />
							Open in new tab
						</label>
					</div>
				</div>
				<div class="drawer-actions">
					<button class="btn btn-secondary" @click="closeLinkDrawer">Cancel</button>
					<button class="btn btn-primary" :disabled="!isLinkSaveable" @click="saveLink">Save</button>
				</div>
			</div>
		</div>

		<!-- Code Drawer -->
		<div v-if="codeDrawerOpen" class="drawer-overlay" @click="closeCodeDrawer">
			<div class="drawer" @click.stop>
				<div class="drawer-header">
					<h3>Source Code</h3>
					<button class="close-btn" @click="closeCodeDrawer">×</button>
				</div>
				<div class="drawer-content">
					<textarea v-model="code" class="code-textarea" placeholder="Enter HTML code"></textarea>
				</div>
				<div class="drawer-actions">
					<button class="btn btn-secondary" @click="closeCodeDrawer">Cancel</button>
					<button class="btn btn-primary" @click="saveCode">Save</button>
				</div>
			</div>
		</div>

		<!-- Image Drawer -->
		<div v-if="imageDrawerOpen" class="drawer-overlay" @click="closeImageDrawer">
			<div class="drawer" @click.stop>
				<div class="drawer-header">
					<h3>Image</h3>
					<button class="close-btn" @click="closeImageDrawer">×</button>
				</div>
				<div class="drawer-content">
					<template v-if="imageSelection">
						<img v-if="imageSelection.previewUrl" class="image-preview" :src="imageSelection.previewUrl" />
						<div class="field">
							<label>Image URL</label>
							<input v-model="imageSelection.imageUrl" class="input" />
						</div>
						<div class="field">
							<label>Alt Text</label>
							<input v-model="imageSelection.alt" class="input" />
						</div>
						<div class="field">
							<label>Width</label>
							<input v-model="imageSelection.width" type="number" class="input" />
						</div>
						<div class="field">
							<label>Height</label>
							<input v-model="imageSelection.height" type="number" class="input" />
						</div>
						<div class="field">
							<label>
								<input type="checkbox" v-model="imageSelection.lazy" />
								Lazy Loading
							</label>
						</div>
					</template>
					<div v-else class="upload-area">
						<input type="file" @change="onImageSelect" accept="image/*" class="file-input" />
						<div class="upload-text">Click to select image or drag and drop</div>
					</div>
				</div>
				<div class="drawer-actions">
					<button class="btn btn-secondary" @click="closeImageDrawer">Cancel</button>
					<button class="btn btn-primary" @click="saveImage">Save</button>
				</div>
			</div>
		</div>

		<!-- Media Drawer -->
		<div v-if="mediaDrawerOpen" class="drawer-overlay" @click="closeMediaDrawer">
			<div class="drawer" @click.stop>
				<div class="drawer-header">
					<h3>Media</h3>
					<button class="close-btn" @click="closeMediaDrawer">×</button>
				</div>
				<div class="drawer-content">
					<div class="tabs">
						<button 
							:class="['tab-btn', { active: openMediaTab === 'video' }]" 
							@click="openMediaTab = 'video'"
						>
							Media
						</button>
						<button 
							:class="['tab-btn', { active: openMediaTab === 'embed' }]" 
							@click="openMediaTab = 'embed'"
						>
							Embed
						</button>
					</div>
					
					<div v-if="openMediaTab === 'video'" class="tab-content">
						<template v-if="mediaSelection">
							<video v-if="mediaSelection.tag !== 'iframe'" class="media-preview" controls>
								<source :src="mediaSelection.previewUrl" />
							</video>
							<iframe
								v-if="mediaSelection.tag === 'iframe'"
								class="media-preview"
								:src="mediaSelection.previewUrl"
								title="Media preview"
							></iframe>
							<div class="field">
								<label>Source</label>
								<input v-model="mediaSource" class="input" />
							</div>
							<div class="field">
								<label>Width</label>
								<input v-model="mediaWidth" type="number" class="input" />
							</div>
							<div class="field">
								<label>Height</label>
								<input v-model="mediaHeight" type="number" class="input" />
							</div>
						</template>
						<div v-else class="upload-area">
							<input type="file" @change="onMediaSelect" accept="video/*,audio/*" class="file-input" />
							<div class="upload-text">Click to select media file or drag and drop</div>
						</div>
					</div>
					
					<div v-if="openMediaTab === 'embed'" class="tab-content">
						<div class="field">
							<label>Embed Code</label>
							<textarea v-model="embed" class="textarea" placeholder="Paste embed code here"></textarea>
						</div>
					</div>
				</div>
				<div class="drawer-actions">
					<button class="btn btn-secondary" @click="closeMediaDrawer">Cancel</button>
					<button class="btn btn-primary" @click="saveMedia">Save</button>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup lang="ts">
import { SettingsStorageAssetPreset } from '@directus/types';
import Editor from '@tinymce/tinymce-vue';
import { cloneDeep, isEqual } from 'lodash';
import { ComponentPublicInstance, computed, onMounted, ref, toRefs, watch } from 'vue';
import tinymce from 'tinymce/tinymce';

import 'tinymce/skins/ui/oxide/skin.css';
import './tinymce-overrides.css';

import 'tinymce/tinymce';

import 'tinymce/icons/default';
import 'tinymce/models/dom';
import 'tinymce/plugins/autoresize/plugin';
import 'tinymce/plugins/code/plugin';
import 'tinymce/plugins/directionality/plugin';
import 'tinymce/plugins/fullscreen/plugin';
import 'tinymce/plugins/image/plugin';
import 'tinymce/plugins/insertdatetime/plugin';
import 'tinymce/plugins/link/plugin';
import 'tinymce/plugins/lists/plugin';
import 'tinymce/plugins/media/plugin';
import 'tinymce/plugins/pagebreak/plugin';
import 'tinymce/plugins/preview/plugin';
import 'tinymce/plugins/table/plugin';
import 'tinymce/themes/silver';

// Import local composables
import useImage from './useImage';
import useLink from './useLink';
import useMedia from './useMedia';
import useSourceCode from './useSourceCode';
import usePre from './usePre';
import useInlineCode from './useInlineCode';
import getEditorStyles from './get-editor-styles';
import toolbarDefault from './toolbar-default';

declare global {
  interface Window {
    MathJax?: {
      typesetPromise?: (elements?: Element[]) => Promise<void>;
      typesetClear?: () => void;
      tex?: {
        inlineMath?: string[][];
        displayMath?: string[][];
        processEscapes?: boolean;
      };
      svg?: {
        fontCache?: string;
      };
    };
  }
}

window.MathJax = {
  tex: {
    inlineMath: [['\\(', '\\)']],
    displayMath: [['$$', '$$']],
    processEscapes: true
  },
  svg: { fontCache: 'global' }
};

type CustomFormat = {
	title: string;
	inline: string;
	classes: string;
	styles: Record<string, string>;
	attributes: Record<string, string>;
};

const props = withDefaults(
	defineProps<{
		value: string | null;
		field?: string;
		toolbar?: string[];
		font?: 'sans-serif' | 'serif' | 'monospace';
		customFormats?: CustomFormat[];
		tinymceOverrides?: Record<string, unknown>;
		disabled?: boolean;
		imageToken?: string;
		folder?: string;
		softLength?: number;
		direction?: string;
	}>(),
	{
		toolbar: () => toolbarDefault,
		font: 'sans-serif',
		customFormats: () => [],
	},
);

const emit = defineEmits(['input']);

const editorRef = ref<any | null>(null);
const editorElement = ref<ComponentPublicInstance | null>(null);
const editorKey = ref(0);

const { imageToken } = toRefs(props);

// Mock settings store for extension compatibility
const storageAssetTransform = ref('all');
const storageAssetPresets = ref<SettingsStorageAssetPreset[]>([]);

const count = ref(0);

// Use composables
const { imageDrawerOpen, imageSelection, closeImageDrawer, onImageSelect, saveImage, imageButton } = useImage(
	editorRef,
	imageToken!,
	{
		storageAssetTransform,
		storageAssetPresets,
	},
);

const {
	mediaDrawerOpen,
	mediaSelection,
	closeMediaDrawer,
	openMediaTab,
	onMediaSelect,
	embed,
	saveMedia,
	mediaHeight,
	mediaWidth,
	mediaSource,
	mediaButton,
} = useMedia(editorRef, imageToken!);

const { linkButton, linkDrawerOpen, closeLinkDrawer, saveLink, linkSelection, isLinkSaveable } = useLink(editorRef);

const { codeDrawerOpen, code, closeCodeDrawer, saveCode, sourceCodeButton } = useSourceCode(editorRef);

const { preButton } = usePre(editorRef);
const { inlineCodeButton } = useInlineCode(editorRef);

const internalValue = computed({
	get() {
		return props.value || '';
	},
	set(value: string) {
		if (props.value !== value) {
			contentUpdated();
		}
	},
});

const editorInitialized = ref(false);
const mathJaxReady = ref(false);

const editorDisabled = computed(() => {
	if (!editorInitialized.value) return false;
	return props.disabled;
});

// Simplified percentage function for extension compatibility
function percentage(value: number, max: number): number {
	if (!max) return 100;
	return Math.round((value / max) * 100);
}

const percRemaining = computed(() => percentage(count.value, props.softLength || 0) ?? 100);

let emittedValue: any;
let isUpdatingContent = false;
let renderTimeout: number | null = null;
let lastRenderTime = 0;
let contentUpdateTimeout: number | null = null;
const RENDER_DEBOUNCE_MS = 2000; // 2 second debounce for better performance
const CONTENT_UPDATE_DEBOUNCE_MS = 300; // 300ms debounce for content updates

function setCount() {
	// Only count if softLength is set (performance optimization)
	if (!props.softLength) return;
	
	const iframeContents = editorRef.value?.contentWindow.document.getElementById('tinymce');
	count.value = iframeContents?.textContent?.replace('\n', '')?.length ?? 0;
}

function contentUpdated() {
	if (isUpdatingContent) return;
	
	// Clear existing timeout
	if (contentUpdateTimeout) {
		clearTimeout(contentUpdateTimeout);
	}
	
	// Debounce content updates to reduce performance impact
	contentUpdateTimeout = window.setTimeout(() => {
		setCount();
		
		const newValue = editorRef.value?.getContent ? editorRef.value.getContent() : null;
		
		if (newValue === emittedValue) return;
		
		emittedValue = newValue;
		emit('input', newValue);
	}, CONTENT_UPDATE_DEBOUNCE_MS);
}

function setupContentWatcher() {
	// No longer using MutationObserver - using event-driven approach instead
	// This function is kept for compatibility but does nothing
	console.log('[Performance] Content watcher setup - using event-driven approach');
}

// Smart event-driven content tracking - replaces heavy MutationObserver
function setupSmartContentTracking(editor: any) {
	console.log('[Performance] Setting up smart content tracking');
	
	// Track math elements count to detect changes
	let lastMathCount = 0;
	
	// Only track specific events that matter
	const eventsToTrack = [
		'keyup', 'paste', 'drop', 'input', 'change', 'ExecCommand', 'SetContent'
	];
	
	eventsToTrack.forEach(eventName => {
		editor.on(eventName, (e: any) => {
			// Skip if we're currently updating content
			if (isUpdatingContent) return;
			
			// Check if math content changed
			const body = editor.getBody();
			if (body) {
				const currentMathCount = body.querySelectorAll('span.math-tex').length;
				
				// Only trigger content update if math count changed or it's a significant event
				if (currentMathCount !== lastMathCount || 
					eventName === 'paste' || 
					eventName === 'drop' || 
					eventName === 'SetContent') {
					
					lastMathCount = currentMathCount;
					contentUpdated();
					
					// Auto-render only if math was added
					if (currentMathCount > lastMathCount && mathJaxReady.value) {
						debouncedRenderAllMath();
					}
				}
			}
		});
	});
	
	// Special handling for math insertion
	editor.on('ObjectSelected', (e: any) => {
		if (e.target && e.target.classList && e.target.classList.contains('math-tex')) {
			// Math element was selected - no need to do anything special
			console.log('[Performance] Math element selected');
		}
	});
	
	console.log('[Performance] Smart content tracking setup complete');
}

// --- Math helpers ---
function encodeTex(tex: string) {
  return tex.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

function decodeTex(tex: string) {
  const txt = document.createElement('textarea');
  txt.innerHTML = tex;
  return txt.value;
}

function insertMathPlaceholder(editor: any, tex: string, display = false) {
	console.log('[MathJax] Inserting math placeholder:', tex, 'display:', display);
	
	const delimit = display ? `$$${tex}$$` : `\\(${tex}\\)`;
	const spanHtml = `<span class="math-tex" contenteditable="false" data-tex="${encodeTex(
		tex,
	)}" data-display="${display ? 'true' : 'false'}">${delimit}</span>&nbsp;`;
	editor.insertContent(spanHtml);
	
	// Trigger content update immediately for math insertion
	contentUpdated();
	
	// Auto-render the newly inserted math after a longer delay for better performance
	setTimeout(() => {
		console.log('[MathJax] Attempting to render math. mathJaxReady:', mathJaxReady.value);
		
		if (mathJaxReady.value) {
			const win = editor.getWin();
			const body = editor.getBody();
			if (body && win?.MathJax?.typesetPromise) {
				// Find the newly inserted math element and render just that
				const mathElements = body.querySelectorAll('span.math-tex');
				const lastMathElement = mathElements[mathElements.length - 1];
				console.log('[MathJax] Found math elements:', mathElements.length, 'last element:', lastMathElement);
				
				if (lastMathElement) {
					console.log('[MathJax] Rendering math element:', lastMathElement.textContent);
					// Use requestIdleCallback for better performance if available
					const renderMath = () => {
						win.MathJax.typesetPromise([lastMathElement])
							.then(() => {
								console.log('[MathJax] Successfully rendered math');
							})
							.catch((err: any) => {
								console.error("[MathJax] Error rendering new math:", err);
							});
					};
					
					if (window.requestIdleCallback) {
						window.requestIdleCallback(renderMath, { timeout: 1000 });
					} else {
						renderMath();
					}
				}
			} else {
				console.warn('[MathJax] MathJax not available in iframe');
			}
		} else {
			console.warn('[MathJax] MathJax not ready');
		}
	}, 200); // Increased delay for better performance
}

function renderAllMath() {
  console.log("[MathJax] Starting renderAllMath...");
  if (!editorRef.value || !mathJaxReady.value) {
    console.warn("[MathJax] Editor or MathJax not ready");
    return;
  }

  isUpdatingContent = true;

  const body = editorRef.value.getBody();
  const win = editorRef.value.getWin();
  if (!body || !win) {
    console.warn("[MathJax] No editor body or window found");
    isUpdatingContent = false;
    return;
  }

  // Check if there are any math elements to render
  const mathElements = body.querySelectorAll('span.math-tex[data-tex]');
  if (mathElements.length === 0) {
    console.log("[MathJax] No math elements to render");
    isUpdatingContent = false;
    return;
  }

  // Restore raw TeX before rendering
  mathElements.forEach((span : any) => {
    const tex = decodeTex(span.getAttribute('data-tex') || '');
    const display = span.getAttribute('data-display') === 'true';
    span.textContent = display ? `$$${tex}$$` : `\\(${tex}\\)`;
  });

  // Clear previous render
  if (win.MathJax?.typesetClear) {
    win.MathJax.typesetClear();
  }

  // Typeset with performance optimization
  if (win.MathJax?.typesetPromise) {
    const renderMath = () => {
      win.MathJax.typesetPromise([body])
        .then(() => console.log("[MathJax] Typesetting complete."))
        .catch((err: any) => console.error("[MathJax] Error during typesetPromise:", err))
        .finally(() => { isUpdatingContent = false; });
    };
    
    // Use requestIdleCallback for better performance if available
    if (window.requestIdleCallback) {
      window.requestIdleCallback(renderMath, { timeout: 2000 });
    } else {
      // Fallback to setTimeout for better performance
      setTimeout(renderMath, 50);
    }
  } else {
    console.error("[MathJax] typesetPromise not available");
    isUpdatingContent = false;
  }
}

// Debounced render function for better performance
function debouncedRenderAllMath() {
  const now = Date.now();
  
  // Clear existing timeout
  if (renderTimeout) {
    clearTimeout(renderTimeout);
  }
  
  // If we just rendered recently, don't render again
  if (now - lastRenderTime < RENDER_DEBOUNCE_MS) {
    renderTimeout = window.setTimeout(() => {
      renderAllMath();
      lastRenderTime = Date.now();
    }, RENDER_DEBOUNCE_MS);
  } else {
    renderAllMath();
    lastRenderTime = now;
  }
}

function replaceDelimitersInNode(rootNode: Node) {
  const doc = rootNode.ownerDocument || (rootNode as any).document;
  if (!doc) return;

  function isSkippable(node: Node) {
    const el = node as Element;
    return !!(el?.closest && (el.closest('pre') || el.closest('code') || el.closest('.math-tex')));
  }

  function walk(node: Node) {
    if (isSkippable(node)) return;

    if (node.nodeType === Node.TEXT_NODE) {
      const text = node.nodeValue || '';
      if (!text.trim()) return;

      let newNodes: Node[] = [];
      let cursor = 0;

      // Patterns for math
      const patterns = [
        { regex: /\$\$([\s\S]+?)\$\$/g, display: true },       // $$ ... $$
        { regex: /\\\[([\s\S]+?)\\\]/g, display: true },       // \[ ... \]
        { regex: /\\\(([\s\S]+?)\\\)/g, display: false },      // \( ... \)
        { regex: /(?<!\$)\$([\s\S]+?)\$(?!\$)/g, display: false } // $ ... $
      ];

      while (cursor < text.length) {
        let earliestMatch: any = null;
        let earliestIndex = text.length;

        for (const pattern of patterns) {
          pattern.regex.lastIndex = cursor;
          const match = pattern.regex.exec(text);
          if (match && match.index < earliestIndex) {
            earliestMatch = { ...match, display: pattern.display };
            earliestIndex = match.index;
          }
        }

        if (!earliestMatch) {
          newNodes.push(doc.createTextNode(text.slice(cursor)));
          break;
        }

        // Add text before match
        if (earliestMatch.index > cursor) {
          newNodes.push(doc.createTextNode(text.slice(cursor, earliestMatch.index)));
        }

        // Math placeholder
        const tex = earliestMatch[1];
        const span = doc.createElement('span');
        span.className = 'math-tex';
        span.setAttribute('contenteditable', 'false');
        span.setAttribute('data-tex', encodeTex(tex));
        span.setAttribute('data-display', earliestMatch.display ? 'true' : 'false');
        span.textContent = earliestMatch.display ? `$$${tex}$$` : `\\(${tex}\\)`;
        newNodes.push(span);

        // Add space after
        newNodes.push(doc.createTextNode('\u00A0'));

        cursor = earliestMatch.index + earliestMatch[0].length;
      }

      const frag = doc.createDocumentFragment();
      newNodes.forEach(n => frag.appendChild(n));
      node.parentNode?.replaceChild(frag, node);
    } else {
      let child = node.firstChild;
      while (child) {
        const next = child.nextSibling;
        walk(child);
        child = next;
      }
    }
  }

  walk(rootNode);
}

function setup(editor: any) {
	editorRef.value = editor;

	const linkShortcut = 'meta+k';

	editor.ui.registry.addToggleButton('customPre', preButton);
	editor.ui.registry.addToggleButton('customImage', imageButton);
	editor.ui.registry.addToggleButton('customMedia', mediaButton);
	editor.ui.registry.addToggleButton('customLink', { ...linkButton, shortcut: linkShortcut });
	editor.ui.registry.addToggleButton('customInlineCode', inlineCodeButton);
	editor.ui.registry.addButton('customCode', sourceCodeButton);

	// Math button
	editor.ui.registry.addButton('math', {
		text: '∑',
		tooltip: 'Insert Math',
		onAction: () => {
			editor.windowManager.open({
				title: 'Insert LaTeX',
				body: {
					type: 'panel',
					items: [
						{ type: 'textarea', name: 'tex', label: 'LaTeX' },
						{ type: 'checkbox', name: 'display', label: 'Display (block)' }
					]
				},
				buttons: [
					{ type: 'cancel', name: 'cancel', text: 'Cancel' },
					{ type: 'submit', text: 'Insert', primary: true }
				],
				onSubmit: (api: any) => {
					const data = api.getData();
					const tex = (data.tex || '').trim();
					if (!tex) { 
						api.close(); 
						return; 
					}
					insertMathPlaceholder(editor, tex, !!data.display);
					api.close();
				}
			});
		}
	});

	// Render Math button
	editor.ui.registry.addButton('rendermath', {
		text: '🔄',
		tooltip: 'Render Math (Manual)',
		onAction: () => {
			renderAllMath(); // Use immediate render for manual button
		}
	});

	// Handle double-click to edit math
	editor.on('DblClick', function (e: any) {
		try {
			const clicked = e.target?.closest ? e.target.closest('.math-tex') : e.target;
			if (!clicked || !clicked.classList?.contains('math-tex')) return;

			const currentTex = decodeTex(clicked.getAttribute('data-tex') ?? '');
			const dataDisplayAttr = clicked.getAttribute('data-display');
			let displayFlag = dataDisplayAttr === 'true';

			editor.windowManager.open({
				title: 'Edit LaTeX',
				body: {
					type: 'panel',
					items: [
						{ type: 'textarea', name: 'tex', label: 'LaTeX' },
						{ type: 'checkbox', name: 'display', label: 'Display (block)' },
					],
				},
				buttons: [
					{ type: 'cancel', name: 'cancel', text: 'Cancel' },
					{ type: 'submit', text: 'Update', primary: true },
				],
				initialData: {
					tex: currentTex,
					display: displayFlag,
				},
				onSubmit: (api: any) => {
					const data = api.getData();
					const newTex = (data.tex || '').trim();
					if (!newTex) {
						api.close();
						return;
					}

					clicked.setAttribute('data-tex', encodeTex(newTex));
					clicked.setAttribute('data-display', data.display ? 'true' : 'false');
					clicked.textContent = data.display ? `$$${newTex}$$` : `\\(${newTex}\\)`;

					// Re-render this specific element
					const win = editor.getWin();
					if (win?.MathJax?.typesetPromise) {
						win.MathJax.typesetPromise([clicked]).catch((err: any) => {
							console.error("[MathJax] Error rendering edited math:", err);
						});
					}

					api.close();
				},
			});
		} catch (err) {
			console.warn('Double-click edit failed', err);
		}
	});

	editor.on('init', function () {
		editor.shortcuts.remove(linkShortcut);
		editor.addShortcut(linkShortcut, 'Insert Link', () => {
			editor.ui.registry.getAll().buttons.customlink.onAction();
		});

		setCount();
		editorInitialized.value = true;

		// Setup smart event-driven content tracking
		setupSmartContentTracking(editor);

		// Initialize MathJax in editor iframe
		try {
			const doc = editor.getDoc();
			const head = doc.head || doc.getElementsByTagName('head')[0];

			const configScript = doc.createElement('script');
			configScript.type = 'text/javascript';
			configScript.text = `
				window.MathJax = {
					tex: {
						inlineMath: [['$','$'], ['\\\\(','\\\\)']],
						displayMath: [['$$','$$'], ['\\\\[','\\\\]']],
						processEscapes: true,
						processEnvironments: true
					},
					options: {
						skipHtmlTags: ['script','noscript','style','textarea','pre'],
						ignoreHtmlClass: 'tex2jax_ignore',
						processHtmlClass: 'tex2jax_process',
						enableMenu: false, // Disable menu for better performance
						menuOptions: {
							settings: {
								texHints: false,
								semantics: false,
								zoom: 'NoZoom'
							}
						}
					},
					loader: {
						load: ['[tex]/ams']
					},
					startup: {
						pageReady: () => {
							return MathJax.startup.defaultPageReady().then(() => {
								// Disable automatic typesetting for better performance
								MathJax.startup.promise.then(() => {
									MathJax.typesetClear();
									// Disable automatic processing
									MathJax.startup.document.state(0);
								});
							});
						}
					}
				};
			`;
			head.appendChild(configScript);

			const mj = doc.createElement('script');
			mj.type = 'text/javascript';
			mj.src = 'https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js';
			mj.async = true;
			mj.onload = () => {
				mathJaxReady.value = true;
				// Initial render of existing math after a longer delay for better performance
				setTimeout(() => {
					renderAllMath();
				}, 500);
			};
			head.appendChild(mj);
		} catch (err) {
			console.warn('MathJax injection failed:', err);
		}
	});

	// Handle paste events
	editor.on('PastePreProcess', function (e: any) {
		try {
			// Only process if content contains math delimiters
			if (e.content.includes('$') || e.content.includes('\\(') || e.content.includes('\\[')) {
				const parser = new DOMParser();
				const doc = parser.parseFromString(`<div>${e.content}</div>`, 'text/html');
				replaceDelimitersInNode(doc.body);
				const newHtml = doc.body.firstElementChild?.innerHTML ?? e.content;
				e.content = newHtml;
			}
		} catch (err) {
			// fallback - leave content unchanged
		}
	});

	editor.on('OpenWindow', function (e: any) {
		if (e.dialog?.getData) {
			const data = e.dialog?.getData();

			if (data) {
				if (data.url) {
					e.dialog.close();
					editor.ui.registry.getAll().buttons.customlink.onAction();
				}

				if (data.src) {
					e.dialog.close();
					editor.ui.registry.getAll().buttons.customimage.onAction(true);
				}
			}
		}
	});
}

function setFocus(val: boolean) {
	if (editorElement.value == null) return;
	const body = editorElement.value.$el.parentElement?.querySelector('.tox-tinymce');

	if (body == null) return;

	if (val) {
		body.classList.add('focus');
	} else {
		body.classList.remove('focus');
	}
}

const editorOptions = computed(() => {
	const styleFormats =
		Array.isArray(props.customFormats) && props.customFormats.length > 0 ? cloneDeep(props.customFormats) : null;

	let toolbarString = (props.toolbar ?? [])
		.map((button: string) =>
			button
				.replace(/^link$/g, 'customLink')
				.replace(/^media$/g, 'customMedia')
				.replace(/^code$/g, 'customCode')
				.replace(/^image$/g, 'customImage')
				.replace(/^pre$/g, 'customPre')
				.replace(/^inlinecode$/g, 'customInlineCode'),
		)
		.join(' ');
		
	if (!toolbarString.includes('math')) {
  		toolbarString += ' math';
	}
	
	if (!toolbarString.includes('rendermath')) {
  		toolbarString += ' rendermath';
	}

	if (styleFormats) {
		toolbarString += ' styles';
	}

	return {
		skin: false,
		content_css: false,
		content_style: getEditorStyles(props.font as 'sans-serif' | 'serif' | 'monospace'),
		plugins: [
			'media',
			'table',
			'lists',
			'image',
			'link',
			'pagebreak',
			'code',
			'insertdatetime',
			'autoresize',
			'preview',
			'fullscreen',
			'directionality',
		],
		branding: false,
		max_height: 1000,
		elementpath: false,
		statusbar: false,
		menubar: false,
		convert_urls: false,
		image_dimensions: false,
		extended_valid_elements: 'audio[loop|controls],source[src|type]',
		toolbar: toolbarString ? toolbarString : false,
		style_formats: styleFormats,
		file_picker_types: 'customImage customMedia image media',
		link_default_protocol: 'https',
		browser_spellcheck: true,
		directionality: props.direction,
		paste_data_images: false,
		setup,
		language: 'en',
		ui_mode: 'split',
		...(props.tinymceOverrides && cloneDeep(props.tinymceOverrides)),
	};
});

watch(
	() => [props.direction, editorRef],
	() => {
		if (editorRef.value) {
			if (props.direction === 'rtl') {
				editorRef.value.editorCommands?.commands?.exec?.mcedirectionrtl();
			} else {
				editorRef.value.editorCommands?.commands?.exec?.mcedirectionltr();
			}
		}
	},
);

watch(
	() => [props.toolbar, props.font, props.customFormats, props.tinymceOverrides],
	(newOptions: any, oldOptions: any) => {
		if (isEqual(newOptions, oldOptions)) return;

		// Cleanup timeouts
		if (renderTimeout) {
			clearTimeout(renderTimeout);
			renderTimeout = null;
		}
		if (contentUpdateTimeout) {
			clearTimeout(contentUpdateTimeout);
			contentUpdateTimeout = null;
		}

		editorRef.value.remove();
		editorInitialized.value = false;
		mathJaxReady.value = false;
		editorKey.value++;
	},
);
</script>

<style lang="scss" scoped>
.wysiwyg {
	position: relative;
}

.remaining {
	position: absolute;
	inset-inline-end: 10px;
	inset-block-end: 5px;
	color: var(--theme--form--field--input--foreground-subdued);
	font-weight: 600;
	text-align: end;
	vertical-align: middle;
	font-feature-settings: 'tnum';
}

.warning {
	color: var(--theme--warning);
}

.danger {
	color: var(--theme--danger);
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
}

/* Drawer styles */
.drawer-overlay {
	position: fixed;
	top: 0;
	left: 0;
	right: 0;
	bottom: 0;
	background: rgba(0, 0, 0, 0.5);
	z-index: 1000;
	display: flex;
	align-items: center;
	justify-content: center;
}

.drawer {
	background: white;
	border-radius: 8px;
	box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
	max-width: 500px;
	width: 90%;
	max-height: 80vh;
	overflow: hidden;
	display: flex;
	flex-direction: column;
}

.drawer-header {
	padding: 20px;
	border-bottom: 1px solid #eee;
	display: flex;
	justify-content: space-between;
	align-items: center;
}

.drawer-header h3 {
	margin: 0;
	font-size: 18px;
	font-weight: 600;
}

.close-btn {
	background: none;
	border: none;
	font-size: 24px;
	cursor: pointer;
	color: #666;
	padding: 0;
	width: 30px;
	height: 30px;
	display: flex;
	align-items: center;
	justify-content: center;
	border-radius: 4px;
}

.close-btn:hover {
	background: #f5f5f5;
}

.drawer-content {
	padding: 20px;
	flex: 1;
	overflow-y: auto;
}

.drawer-actions {
	padding: 20px;
	border-top: 1px solid #eee;
	display: flex;
	gap: 10px;
	justify-content: flex-end;
}

.field {
	margin-bottom: 20px;
}

.field label {
	display: block;
	margin-bottom: 8px;
	font-weight: 500;
	color: #333;
}

.input, .textarea {
	width: 100%;
	padding: 10px;
	border: 1px solid #ddd;
	border-radius: 4px;
	font-size: 14px;
	box-sizing: border-box;
}

.textarea {
	min-height: 100px;
	resize: vertical;
}

.code-textarea {
	font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
	font-size: 13px;
	line-height: 1.4;
}

.btn {
	padding: 10px 20px;
	border: none;
	border-radius: 4px;
	font-size: 14px;
	font-weight: 500;
	cursor: pointer;
	transition: all 0.2s ease;
}

.btn-primary {
	background: #007cba;
	color: white;
}

.btn-primary:hover:not(:disabled) {
	background: #005a87;
}

.btn-primary:disabled {
	background: #ccc;
	cursor: not-allowed;
}

.btn-secondary {
	background: #f5f5f5;
	color: #333;
	border: 1px solid #ddd;
}

.btn-secondary:hover {
	background: #e8e8e8;
}

.image-preview, .media-preview {
	width: 100%;
	height: 200px;
	margin-bottom: 20px;
	object-fit: cover;
	border-radius: 4px;
	border: 1px solid #eee;
}

.upload-area {
	border: 2px dashed #ddd;
	border-radius: 8px;
	padding: 40px 20px;
	text-align: center;
	cursor: pointer;
	transition: all 0.2s ease;
}

.upload-area:hover {
	border-color: #007cba;
	background: #f8f9ff;
}

.upload-text {
	color: #666;
	font-size: 14px;
}

.file-input {
	position: absolute;
	opacity: 0;
	width: 100%;
	height: 100%;
	cursor: pointer;
}

.tabs {
	display: flex;
	border-bottom: 1px solid #eee;
	margin-bottom: 20px;
}

.tab-btn {
	padding: 10px 20px;
	background: none;
	border: none;
	border-bottom: 2px solid transparent;
	cursor: pointer;
	font-size: 14px;
	color: #666;
	transition: all 0.2s ease;
}

.tab-btn.active {
	color: #007cba;
	border-bottom-color: #007cba;
}

.tab-btn:hover {
	color: #333;
}

.tab-content {
	min-height: 200px;
}
</style>
