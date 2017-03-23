if (CKEDITOR.env.ie && CKEDITOR.env.version < 9)
	CKEDITOR.tools.enableHtml5Elements(document);

CKEDITOR.config.height = 'auto';
CKEDITOR.config.width = 'auto';

var editorInit = (function() {
	var wysiwygareaAvailable = isWysiwygareaAvailable(),
		isBBCodeBuiltIn = !!CKEDITOR.plugins.get('bbcode');

	return function() {
		var editorElement = CKEDITOR.document.getById('editor');

		if (wysiwygareaAvailable) {
			CKEDITOR.replace('editor');
		}
		else {
			editorElement.setAttribute('contenteditable', 'true');
			CKEDITOR.inline('editor');
		}
	};

	function isWysiwygareaAvailable() {
		if (CKEDITOR.revision == ('%RE' + 'V%')) {
			return true;
		}

		return !!CKEDITOR.plugins.get('wysiwygarea');
	}
})();

var editorDestory = (function() {
	
	return function() {
		console.log("CKEDITOR Destory");
		for (name in CKEDITOR.instances) {
			CKEDITOR.instances[name].destroy()
		}
	}
})();

var getEditorData = (function() {
	return function() {
		console.log("CKEDITOR GET DATA");
		var data = CKEDITOR.instances.editor.getData();
		return data;
	}
})();
