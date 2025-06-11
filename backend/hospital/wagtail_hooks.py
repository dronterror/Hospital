from wagtail import hooks
from wagtail.admin.rich_text.editors.draftail import features as draftail_features
from wagtail.admin.rich_text.converters.html_to_contentstate import InlineStyleElementHandler
from wagtail.admin.menu import MenuItem
from draftjs_exporter.dom import DOM

@hooks.register('register_rich_text_features')
def register_html_feature(features):
    """
    Register the `html` feature, which uses the `CODE` Draft.js inline style type,
    and is stored as HTML in the database.
    """
    feature_name = 'html'
    type_ = 'HTML'

    # Configure Draftail
    control = {
        'type': type_,
        'icon': 'code',
        'description': 'HTML',
        'style': {'fontFamily': 'monospace'},
    }

    features.register_editor_plugin(
        'draftail', feature_name, draftail_features.InlineStyleFeature(control)
    )

    # Configure the content transform from the DB to the editor and back.
    db_conversion = {
        'from_database_format': {'code[class=html]': InlineStyleElementHandler(type_)},
        'to_database_format': {'style_map': {type_: {'element': 'code', 'props': {'class': 'html'}}}},
    }

    features.register_converter_rule('contentstate', feature_name, db_conversion)

    # This will register html as a feature that is allowed in rich text areas
    features.default_features.append(feature_name)

@hooks.register('register_rich_text_features')
def register_raw_html_features(features):
    """Register the raw HTML button in the rich text editor."""
    feature_name = 'raw_html'
    type_ = 'RAW_HTML'
    
    control = {
        'type': type_,
        'label': 'Raw HTML',
        'icon': 'code',
        'description': 'Raw HTML Editor',
    }
    
    features.register_editor_plugin(
        'draftail',
        feature_name,
        draftail_features.InlineStyleFeature(control)
    )
    
    features.default_features.append(feature_name)

@hooks.register('insert_editor_css')
def editor_css():
    """Add custom CSS to the admin."""
    return """
        <style>
            .Draftail-Editor .raw-html {
                font-family: monospace;
                background-color: #f8f9fa;
                padding: 2px 4px;
                border-radius: 3px;
            }
        </style>
    """

@hooks.register('construct_page_action_menu')
def add_html_editor_menu_item(menu_items, request, context):
    """Add HTML editor button to the page action menu."""
    menu_items.append(
        MenuItem(
            label='HTML Editor',
            name='html-editor',
            icon_name='code',
            classnames='action-html-editor',
            order=200
        )
    )

@hooks.register('insert_editor_js')
def editor_js():
    """Add custom JavaScript to the admin."""
    return """
        <script>
            window.addEventListener('load', function() {
                // Add HTML editor button functionality
                document.querySelectorAll('[data-draftail-input]').forEach(function(editor) {
                    editor.addEventListener('click', function(e) {
                        if (e.target.closest('.action-html-editor')) {
                            // Toggle HTML view
                            var content = editor.querySelector('.Draftail-Editor__content');
                            if (content) {
                                content.classList.toggle('show-html');
                            }
                        }
                    });
                });
            });
        </script>
    """ 