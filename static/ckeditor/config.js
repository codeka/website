/**
 * @license Copyright (c) 2003-2012, CKSource - Frederico Knabben. All rights reserved.
 * For licensing, see LICENSE.html or http://ckeditor.com/license
 */

CKEDITOR.stylesSet.add('code_styles', [
    { name: 'Normal', element: 'p', attributes: { 'class': '' } },
    { name: 'Java', element: 'pre', attributes: { 'class': 'brush: java;' } },
    { name: 'JavaScript', element: 'pre', attributes: { 'class': 'brush: js' } },
    { name: 'C++', element: 'pre', attributes: { 'class': 'brush: cpp' } },
    { name: 'C#', element: 'pre', attributes: { 'class': 'brush: csharp' } },
    { name: 'CSS', element: 'pre', attributes: { 'class': 'brush: css' } },
    { name: 'PHP', element: 'pre', attributes: { 'class': 'brush: php' } },
    { name: 'Plain Text', element: 'pre', attributes: { 'class': 'brush: text' } },
    { name: 'Python', element: 'pre', attributes: { 'class': 'brush: python' } },
    { name: 'SQL', element: 'pre', attributes: { 'class': 'brush: sql' } },
    { name: 'XML/HTML', element: 'pre', attributes: { 'class': 'brush: xml' } }
]);

CKEDITOR.editorConfig = function( config ) {

	// The toolbar groups arrangement, optimized for a single toolbar row.
	config.toolbarGroups = [
		{ name: 'document',	   groups: [ 'mode', 'document', 'doctools' ] },
		{ name: 'editing',     groups: [ 'find', 'selection', 'spellchecker' ] },
		{ name: 'forms' },
		{ name: 'basicstyles', groups: [ 'basicstyles', 'cleanup' ] },
		{ name: 'paragraph',   groups: [ 'list', 'indent', 'blocks', 'align' ] },
		{ name: 'links' },
		{ name: 'insert' },
		{ name: 'styles' },
		{ name: 'colors' },
		{ name: 'tools' },
		{ name: 'others' },
	];

	   // The default plugins included in the basic setup define some buttons that
	   // we don't want to have in a basic editor. We remove them here.
	   config.removeButtons = 'Anchor,Underline,Strike,Subscript,Superscript';

	   // Considering that the basic setup doesn't provide pasting cleanup features,
	   // it's recommended to force everything to be plain text.
	   config.forcePasteAsPlainText = true;

	   // Let's have it basic on dialogs as well.
	   config.removeDialogTabs = 'link:advanced';

    // We'll use our custom CSS, so that it looks similar to the rest of the site.
    config.contentsCss = '/v1/css/wysiwyg_editor.css';

    // allow all html tags, we sanitize this on the server anyway
    config.allowedContent = true;

    config.stylesSet = 'code_styles';
};
