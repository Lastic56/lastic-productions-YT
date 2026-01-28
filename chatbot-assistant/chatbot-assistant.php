<?php
/**
 * Plugin Name: Chatbot Assistant
 * Description: A modern, interactive chatbot assistant with OpenAI, Ollama, and LM Studio integrations.
 * Version: 1.0.0
 * Author: Antigravity
 * Text Domain: chatbot-assistant
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit; // Exit if accessed directly.
}

// Define constants
define( 'CBA_PLUGIN_DIR', plugin_dir_path( __FILE__ ) );
define( 'CBA_PLUGIN_URL', plugin_dir_url( __FILE__ ) );

// Include required files
require_once CBA_PLUGIN_DIR . 'includes/admin-settings.php';
require_once CBA_PLUGIN_DIR . 'includes/chat-handler.php';

// Initialize the plugin
add_action( 'plugins_loaded', 'cba_init' );

function cba_init() {
	// Initialize admin settings
	if ( is_admin() ) {
		new CBA_Admin_Settings();
	}

	// Initialize Chat Handler
	new CBA_Chat_Handler();
}

// Enqueue styles and scripts for frontend
add_action( 'wp_enqueue_scripts', 'cba_enqueue_scripts' );

function cba_enqueue_scripts() {
	wp_enqueue_style( 'cba-chat-style', CBA_PLUGIN_URL . 'assets/css/chat-widget.css', array(), '1.0.0' );
	wp_enqueue_script( 'cba-chat-script', CBA_PLUGIN_URL . 'assets/js/chat-widget.js', array( 'jquery' ), '1.0.0', true );

	// Localize script for AJAX
	wp_localize_script( 'cba-chat-script', 'cba_ajax', array(
		'ajax_url' => admin_url( 'admin-ajax.php' ),
		'nonce'    => wp_create_nonce( 'cba_chat_nonce' ),
        'settings' => get_option( 'cba_settings', array() )
	) );
}

// Register frontend widget container
add_action( 'wp_footer', 'cba_render_chat_container' );

function cba_render_chat_container() {
    $settings = get_option( 'cba_settings', array() );
    $bot_name = !empty($settings['bot_name']) ? esc_html($settings['bot_name']) : 'Assistant';
    $greeting = !empty($settings['greeting']) ? esc_html($settings['greeting']) : 'Hello! How can I help you today?';
	?>
	<div id="cba-chat-container" class="cba-closed">
		<button id="cba-chat-toggle" title="Open Chat">
			<span class="cba-icon-chat">💬</span>
		</button>
		<div id="cba-chat-window">
			<div id="cba-chat-header">
				<span class="cba-bot-name"><?php echo $bot_name; ?></span>
				<button id="cba-chat-close">×</button>
			</div>
			<div id="cba-chat-messages">
				<div class="cba-message cba-bot">
					<div class="cba-content"><?php echo $greeting; ?></div>
				</div>
			</div>
			<div id="cba-chat-input-area">
				<input type="text" id="cba-chat-input" placeholder="Type a message..." autocomplete="off">
				<button id="cba-chat-send">Send</button>
			</div>
		</div>
	</div>
	<?php
}
