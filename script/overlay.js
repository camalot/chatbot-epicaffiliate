"use strict";
let animationEndClasses = "webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend";
if (!window.settings) {
	window.settings = {};
}

window.settings = { ...window.DEFAULT_SETTINGS, ...window.settings };

function initializeUI() {
	
	var fontName = settings.FontName;
	var customFontName = settings.CustomFontName;
	if (fontName && fontName === "custom" && customFontName && customFontName !== "") {
		loadFontsScript(customFontName);
	} else {
		$(":root").css("--font-name", fontName);
	}

	let backgroundImage = "none";

	if (settings.BackgroundImage && settings.BackgroundImage !== "") {
		backgroundImage = `url('${settings.BackgroundImage}')`;
	}
	
	$(":root")
		.css("--body-opacity", `${(settings.Opacity || 100) / 100}`)
		.css("--title-font-size", `${settings.TitleFontSize || 2}em`)
		.css("--help-font-size", `${settings.HelpFontSize || 1.5}em`)
		.css("--bg-color", `${settings.BackgroundColor || "rgba(0, 0, 0, 1)"}`)
		.css("--background-image", backgroundImage)
		.css("--img-bg-color", `${settings.ImageBackgroundColor || "rgba(0, 0, 0, 1)"}`)
		.css("--outline-color", `${settings.OutlineColor || "rgba(240, 240, 240, 1)"}`)
		.css("--text-color", `${settings.TextColor || "rgba(255, 255, 255, 1)"}`)
		.css("--command-color", `${settings.CommandColor || "rgba(153, 74, 0, 1)"}`)

		.css("--box-border-radius-topright", `${settings.BoxBorderRadiusTopRight || 0}px`)
		.css("--box-border-radius-topleft", `${settings.BoxBorderRadiusTopLeft || 0}px`)
		.css("--box-border-radius-bottomright", `${settings.BoxBorderRadiusBottomRight || 0}px`)
		.css("--box-border-radius-bottomleft", `${settings.BoxBorderRadiusBottomLeft || 0}px`)
		
		.css("--help-margin-top", `${settings.HelpMarginTop}px`)
		.css("--help-margin-bottom", `${settings.HelpMarginBottom}px`)
		.css("--help-margin-left", `${settings.HelpMarginLeft}px`)
		.css("--help-margin-right", `${settings.HelpMarginRight}px`)
		
		.css("--command-margin-top", `${settings.CommandMarginTop}px`)
		.css("--command-margin-bottom", `${settings.CommandMarginBottom}px`)
		.css("--command-margin-left", `${settings.CommandMarginLeft}px`)
		.css("--command-margin-right", `${settings.CommandMarginRight}px`)

		.css("--title-margin-top", `${settings.TitleMarginTop}px`)
		.css("--title-margin-bottom", `${settings.TitleMarginBottom}px`)
		.css("--title-margin-left", `${settings.TitleMarginLeft}px`)
		.css("--title-margin-right", `${settings.TitleMarginRight}px`)

		.css("--icon-margin-top", `${settings.IconMarginTop}px`)
		.css("--icon-margin-bottom", `${settings.IconMarginBottom}px`)
		.css("--icon-margin-left", `${settings.IconMarginLeft}px`)
		.css("--icon-margin-right", `${settings.IconMarginRight}px`)
		;

		if (settings.BackgroundVideo && settings.BackgroundVideo !== "") {
			$("video#ad-bg").attr("src", `${settings.BackgroundVideo}`).removeClass("hidden");
		} else {
			$("video#ad-bg").addClass("hidden");
		}
}

function connectWebsocket() {
	//-------------------------------------------
	//  Create WebSocket
	//-------------------------------------------
	let socket = new WebSocket("ws://127.0.0.1:3337/streamlabs");

	//-------------------------------------------
	//  Websocket Event: OnOpen
	//-------------------------------------------
	socket.onopen = function () {
		// AnkhBot Authentication Information
		let auth = {
			author: "DarthMinos",
			website: "darthminos.tv",
			api_key: API_Key,
			events: [
				"EVENT_EPICAFFILIATE_SETTINGS",
				"EVENT_EPICAFFILIATE_DATA"
			]
		};

		// Send authentication data to ChatBot ws server

		socket.send(JSON.stringify(auth));
	};

	//-------------------------------------------
	//  Websocket Event: OnMessage
	//-------------------------------------------
	socket.onmessage = function (message) {
		console.log(message);
		// Parse message
		let socketMessage = JSON.parse(message.data);
		let eventName = socketMessage.event;
		console.log(socketMessage);
		let eventData = typeof socketMessage.data === "string" ? JSON.parse(socketMessage.data || "{}") : socketMessage.data;
		switch (eventName) {
			case "EVENT_EPICAFFILIATE_DATA":
				// window.EPIC_GAMES = eventData;
				// window.AD_INDEX = 0;

				// runGameRotation();
				break;
			case "EVENT_EPICAFFILIATE_NEXT":
				window.AD_INDEX += 1;
				runGameRotation();
				break;
			case "EVENT_EPICAFFILIATE_PREVIOUS":
				window.AD_INDEX -= 1;
				runGameRotation();
				break;
			case "EVENT_EPICAFFILIATE_SETTINGS":
				window.settings = eventData;
				if (validateInit()) {
					initializeUI();
				}
				break;
			default:
				console.log(eventName);
				break;
		}
	};

	//-------------------------------------------
	//  Websocket Event: OnError
	//-------------------------------------------
	socket.onerror = function (error) {
		console.error(`Error: ${error}`);
	};

	//-------------------------------------------
	//  Websocket Event: OnClose
	//-------------------------------------------
	socket.onclose = function () {
		console.log("close");
		// Clear socket to avoid multiple ws objects and EventHandlings
		socket = null;
		// Try to reconnect every 5s
		setTimeout(function () { connectWebsocket(); }, 5000);
	};

}

function loadFontsScript(font) {
	// bangers;amaranth;allan;bowlby-one;changa-one;days-one;droid-sans;fugaz-one;
	var script = document.createElement('script');
	script.onload = function () {
		$(":root").css("--font-name", font);
	};
	script.src = `http://use.edgefonts.net/${font}.js`;

	document.head.appendChild(script); //or something of the likes
}


function runGameRotation() {
	/*
			<span class="ad-item">
					<span class="icon"><img src="https://cdn2.unrealengine.com/Affiliate+Web%2Fproducts%2FGhostReconBreakpoint_icon-400x400-14a6bb49cd206f65ae33b36b403bd96090081ab4.png" /></span>
					<span class="title">Tom Clancy's Ghost Recon Breakpoint</span>
					<span class="sub-title">Use Command: <code>!link 1</code></span>
			</span>
	*/
	$("#ad-host")
		.queue(function () {
			var gameIndex = Math.floor(Math.random() * window.EPIC_GAMES.length);
			let game = window.EPIC_GAMES[gameIndex];
			console.log(game);
			$("#ad-host .title").html(game.name);
			$("#ad-host .icon img").attr("src", game.icon);
			$("#ad-host .sub-title .message").html(`${settings.CommandMessage}`);
			$("#ad-host .sub-title .command").html(`${settings.Command} ${gameIndex + 1}`);
			$("#ad-host")
				.removeClass()
				.addClass(`${settings.InTransition} animated`)
				.one(animationEndClasses, function () {
					console.log("end in transition")
					$(this)
						.off(animationEndClasses)
						.removeClass()
						.addClass(`${settings.InAttentionAnimation} animated`)
						.one(animationEndClasses, function () {
							$(this)
								.removeClass();
								console.log("end in attention animation");
						});
				})
				.dequeue();
		})
		.delay((settings.DisplaySeconds || 10) * 1000)
		.queue(function () {
			console.log("start out attention");
			$("#ad-host")
				.removeClass()
				.off(animationEndClasses)
				.addClass(`${settings.OutAttentionAnimation} animated`)
				.one(animationEndClasses, function () {
					console.log("end out attention transition");
					$(this)
						.removeClass()
						.addClass(`${settings.OutTransition} animated`)
						.one(animationEndClasses, function () {
							console.log("end out transition")
							$(this)
								.removeClass().addClass("hidden");
						});
				})
				.dequeue();
		})
		.delay((settings.BetweenAdDelay || 10) * 1000)
		.queue(function () {
			// next
			runGameRotation();
			$("#ad-host").dequeue();
		});
}

function validateSettings() {
	let hasApiKey = typeof API_Key !== "undefined";
	let hasSettings = typeof settings !== "undefined";

	return {
		isValid: hasApiKey && hasSettings,
		hasSettings: hasSettings,
		hasApiKey: hasApiKey
	};
}

function validateInit() {
	// verify settings...
	let validatedSettings = validateSettings();

	// Connect if API_Key is inserted
	// Else show an error on the overlay
	if (!validatedSettings.isValid) {
		$("#config-messages").removeClass("hidden");
		$("#config-messages .settings").removeClass(validatedSettings.hasSettings ? "valid" : "hidden");
		$("#config-messages .api-key").removeClass(validatedSettings.hasApiKey ? "valid" : "hidden");
		return false;
	}
	return true;
}

jQuery(document).ready(function () {
	if (validateInit()) {
		initializeUI();

		$.ajax({
			url: "https://cdn.jsdelivr.net/gh/camalot/epic-data-converter@develop/epic.json",
			method: "get",
			dataType: "json",
			success: function (data) {
				window.EPIC_GAMES = data
			},
			complete: function(xhr, status) {
				connectWebsocket();
				runGameRotation();
			},
			error: function(xhr, status, err) {
				console.error(err);
				window.EPIC_GAMES = [];
			}
		});
	} else {
		console.log("Invalid");
	}
});
