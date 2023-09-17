<script>
	import Counter from './Counter.svelte';
	import Role from './Role.svelte';
	import Event from './Event.svelte';
	import Card from './Card.svelte';
	import Chatbox from './Chatbox.svelte';
	import Roundcounter from './Roundcounter.svelte';
	import Othercard from './Othercard.svelte';
	import Othercardplatter from './Othercardplatter.svelte';
	import Othercardplattervote from './Othercardplattervote.svelte';
	import welcome from '$lib/images/svelte-welcome.webp';
	import welcome_fallback from '$lib/images/svelte-welcome.png';

    import { onMount } from 'svelte';
	let role = 0;
	let round = 1;
    async function getData() {
        // Make the API Call here
		role = 2;
		console.log("button clicked");
    }

	var rowdict = {
		0: "President",
		1: "Blue",
		2: "Blue",
		3: "Blue",
		4: "Bomber",
		5: "Red",
		6: "Red",
		7: "Red"
	}

    async function remindRole() {
        // Make the API Call here
		console.log(rowdict[role]);
    }

	let visible = true;
	function toggleVisible(){
		visible = !visible;
	}

	let start = true;
	let vote = false;
	let visible_array = [false, false, false];
	function toggleVisible1(){
		visible_array[0] = !visible_array[0];
		visible_array[1] = 0;
		visible_array[2] = 0;
	}
	function toggleVisible2(){
		visible_array[0] = 0;
		visible_array[1] = !visible_array[1];
		visible_array[2] = 0;
	}
	function toggleVisible3(){
		visible_array[0] = 0;
		visible_array[1] = 0;
		visible_array[2] = !visible_array[2];
	}

	function toggleReset(){
		visible_array[0] = 0;
		visible_array[1] = 0;
		visible_array[2] = 0;
	}

	function toggleStart(){
		start = !start;
	}

	function nextRound(){
		round += 1;
		vote = false;
	}
	function goToVote(){
		
		vote = true;
	}

	let newsFlash = false;

	function goToNormal(){
		newsFlash = false;
	}

</script>

<svelte:head>
	<title>Home</title>
	<meta name="description" content="Svelte demo app" />
</svelte:head>

<section>
	<!--
	<h1>
		<span class="welcome">
			<picture>
				<source srcset={welcome} type="image/webp" />
				<img src={welcome_fallback} alt="Welcome" />
			</picture>
		</span>

		to your new<br />SvelteKit app
	</h1>

	<h2>
		try editing <strong>src/routes/+page.svelte</strong>
	</h2>

	<Counter />
	-->

	{#if newsFlash}
		<Event eventNo={1}/>
		<button on:click={goToNormal}>Ok, noted.</button>
	{:else}

		{#if start}
			<div>
				<button on:click={toggleStart}>PLAY!</button>
			</div>
		{:else}

			{#if vote}

				<Othercardplattervote />

			{:else}

				{#if visible_array[0]}
					<Chatbox resetfn={toggleReset} messages={[["jianzhi", "wang"], ["blah", "blah"]]}/>
				{:else if visible_array[1]}
					<Chatbox resetfn={toggleReset} messages={[["j", "w"], ["b", "b"]]}/>
				{:else if visible_array[2]}
					<Chatbox resetfn={toggleReset} messages={[["joel", "tan"], ["jun", "yao"]]}/>
				{:else}
					<div>
						<div class="roundcounter">
							<h3>
							Round: {round}
						</h3>
							<br>
							<h3>
							Room: A
							</h3>
						</div>
						
						<Othercardplatter fn1={toggleVisible1} fn2={toggleVisible2} fn3={toggleVisible3}/>
						
						<Role />
						
						<Card />
					</div>
					<button on:click={goToVote}>Vote</button>
					<button on:click={nextRound}>Next Round</button>
				{/if}
			{/if}
		{/if}

	{/if}

	<!--<Chatbox />-->
</section>

<style>
	section {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		flex: 0.6;
	}

	h1 {
		width: 100%;
	}

	h3 {
		color: white;
	}

	.welcome {
		display: block;
		position: relative;
		width: 100%;
		height: 0;
		padding: 0 0 calc(100% * 495 / 2048) 0;
	}

	.welcome img {
		position: absolute;
		width: 100%;
		height: 100%;
		top: 0;
		display: block;
	}
</style>
