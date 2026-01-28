<?php
/**
 * Admin Settings for Chatbot Assistant
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

class CBA_Admin_Settings {

	public function __construct() {
		add_action( 'admin_menu', array( $this, 'add_admin_menu' ) );
		add_action( 'admin_init', array( $this, 'settings_init' ) );
        add_action( 'admin_enqueue_scripts', array( $this, 'enqueue_admin_assets' ) );
	}

	public function add_admin_menu() {
		add_menu_page(
			'Chatbot Assistant',
			'Chatbot Assistant',
			'manage_options',
			'chatbot-assistant',
			array( $this, 'settings_page' ),
			'dashicons-format-chat',
			100
		);
	}

    public function enqueue_admin_assets($hook) {
        if ($hook !== 'toplevel_page_chatbot-assistant') return;
        
        wp_enqueue_style('cba-admin-style', CBA_PLUGIN_URL . 'assets/css/admin-settings.css', array(), '1.0.0');
        wp_enqueue_script('cba-admin-script', CBA_PLUGIN_URL . 'assets/js/admin-settings.js', array('jquery'), '1.0.0', true);
        
        wp_localize_script('cba-admin-script', 'cba_admin_ajax', array(
            'ajax_url' => admin_url('admin-ajax.php'),
            'nonce'    => wp_create_nonce('cba_admin_nonce')
        ));
    }

	public function settings_init() {
		register_setting( 'cba_settings_group', 'cba_settings' );

		add_settings_section(
			'cba_general_section',
			'General Settings',
			null,
			'chatbot-assistant'
		);

		add_settings_field(
			'bot_name',
			'Assistant Name',
			array( $this, 'render_text_field' ),
			'chatbot-assistant',
			'cba_general_section',
			array( 'label_for' => 'bot_name' )
		);

		add_settings_field(
			'greeting',
			'Greeting Message',
			array( $this, 'render_textarea_field' ),
			'chatbot-assistant',
			'cba_general_section',
			array( 'label_for' => 'greeting' )
		);

        add_settings_section(
			'cba_ai_section',
			'AI Integration',
			null,
			'chatbot-assistant'
		);

        add_settings_field(
			'ai_service',
			'AI Service',
			array( $this, 'render_select_field' ),
			'chatbot-assistant',
			'cba_ai_section',
			array( 
                'label_for' => 'ai_service',
                'options' => array(
                    'openai' => 'OpenAI',
                    'ollama' => 'Ollama (Local)',
                    'lm-studio' => 'LM Studio (Local)'
                )
            )
		);

        add_settings_field(
			'openai_key',
			'OpenAI API Key',
			array( $this, 'render_text_field' ),
			'chatbot-assistant',
			'cba_ai_section',
			array( 'label_for' => 'openai_key', 'type' => 'password' )
		);

        add_settings_field(
			'local_url',
			'Local Service URL',
			array( $this, 'render_text_field' ),
			'chatbot-assistant',
			'cba_ai_section',
			array( 'label_for' => 'local_url', 'placeholder' => 'http://localhost:11434' )
		);

        add_settings_field(
			'selected_model',
			'Selected Model',
			array( $this, 'render_model_selector' ),
			'chatbot-assistant',
			'cba_ai_section',
			array( 'label_for' => 'selected_model' )
		);
	}

	public function render_text_field( $args ) {
		$options = get_option( 'cba_settings' );
        $type = isset($args['type']) ? $args['type'] : 'text';
        $placeholder = isset($args['placeholder']) ? $args['placeholder'] : '';
		?>
		<input type="<?php echo $type; ?>" 
               name="cba_settings[<?php echo esc_attr( $args['label_for'] ); ?>]" 
               value="<?php echo isset( $options[ $args['label_for'] ] ) ? esc_attr( $options[ $args['label_for'] ] ) : ''; ?>"
               placeholder="<?php echo esc_attr($placeholder); ?>"
               class="regular-text">
		<?php
	}

	public function render_textarea_field( $args ) {
		$options = get_option( 'cba_settings' );
		?>
		<textarea name="cba_settings[<?php echo esc_attr( $args['label_for'] ); ?>]" 
                  rows="3" 
                  class="large-text"><?php echo isset( $options[ $args['label_for'] ] ) ? esc_textarea( $options[ $args['label_for'] ] ) : ''; ?></textarea>
		<?php
	}

    public function render_select_field( $args ) {
        $options = get_option( 'cba_settings' );
        $current = isset( $options[ $args['label_for'] ] ) ? $options[ $args['label_for'] ] : '';
        ?>
        <select name="cba_settings[<?php echo esc_attr( $args['label_for'] ); ?>]" id="<?php echo esc_attr( $args['label_for'] ); ?>">
            <?php foreach($args['options'] as $value => $label): ?>
                <option value="<?php echo esc_attr($value); ?>" <?php selected($current, $value); ?>>
                    <?php echo esc_html($label); ?>
                </option>
            <?php endforeach; ?>
        </select>
        <?php
    }

    public function render_model_selector( $args ) {
        $options = get_option( 'cba_settings' );
        $current_model = isset( $options[ $args['label_for'] ] ) ? $options[ $args['label_for'] ] : '';
        ?>
        <div class="cba-model-selector-wrapper">
            <select name="cba_settings[<?php echo esc_attr( $args['label_for'] ); ?>]" id="cba-model-select">
                <option value="<?php echo esc_attr($current_model); ?>"><?php echo $current_model ? esc_html($current_model) : 'No model selected'; ?></option>
            </select>
            <button type="button" id="cba-fetch-models" class="button button-secondary">Connect & Fetch Models</button>
            <span class="spinner" id="cba-model-spinner"></span>
        </div>
        <?php
    }

	public function settings_page() {
		?>
		<div class="wrap">
			<h1>Chatbot Assistant Settings</h1>
			<form action="options.php" method="post">
				<?php
				settings_fields( 'cba_settings_group' );
				do_settings_sections( 'chatbot-assistant' );
				submit_button();
				?>
			</form>
		</div>
		<?php
	}
}
