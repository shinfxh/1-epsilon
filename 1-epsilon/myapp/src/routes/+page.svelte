<script>
	import Counter from './Counter.svelte';
	import Role from './Role.svelte';
	import Event from './Event.svelte';
	import Card from './Card.svelte';
	import CardSpecial from './CardSpecial.svelte';
	import Chatbox from './Chatbox.svelte';
	import Roundcounter from './Roundcounter.svelte';
	import Othercard from './Othercard.svelte';
	import Othercardplatter from './Othercardplatter.svelte';
	import Othercardplattervote from './Othercardplattervote.svelte';
	import Welcome from './Welcome.svelte';
	import welcome from '$lib/images/svelte-welcome.webp';
	import welcome_fallback from '$lib/images/svelte-welcome.png';

    import { onMount } from 'svelte';
	let role = 0;
	let round = 1;

	function getRandomInt(max) {
	return Math.floor(Math.random() * max);
	}

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

	let arrayOfNames = ['Cathy', 'Daniel', 'Ethan', 'Felix', 'Grace', 'Hu Yongao', 'Ivan'];

	function shuffle(array) {
		let currentIndex = array.length,  randomIndex;

		// While there remain elements to shuffle.
		while (currentIndex > 0) {

			// Pick a remaining element.
			randomIndex = Math.floor(Math.random() * currentIndex);
			currentIndex--;

			// And swap it with the current element.
			[array[currentIndex], array[randomIndex]] = [
			array[randomIndex], array[currentIndex]];
		}

		return array;
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

	let state = 0;
	// 0: PLAY
	// 1: NORMAL
	// 2: CHAT
	// 3: VOTE
	// 4: NEWS FLASH

	function toggleState(newState){
		if (state == 0){
			role = getRandomInt(8);
			arrayOfNames = shuffle(arrayOfNames);
			console.log(role, rowdict[role]);
		}
		state = newState;
	}

</script>

<svelte:head>
	<title>1-Epsilon</title>
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

	{#if state == 4}
		<Event eventNo={1}/>
		<button on:click={goToNormal}>Ok, noted.</button>
	{:else}

		{#if state == 0}
			<div>
				<Welcome />
				<button on:click={() => toggleState(1)}>PLAY!</button>
			</div>
		{:else}

			{#if state == 3}
				<div>
					<div>
						<h3>
						Round: {round}, Room: A
					</h3>
					</div>
				<div style="width:100%; color:red;">
				<Othercardplattervote namesList={arrayOfNames.slice(0, 3)}/>
				</div>
				<div>
				<CardSpecial role={rowdict[role]} name={"You"} />
				</div>
				<div>
				<button on:click={() => toggleState(3)}>Vote</button>
				</div>div>
				</div>

			{:else}

				{#if visible_array[0]}
					<Chatbox name={arrayOfNames[0]} resetfn={toggleReset} messages={[["jianzhi", "wang"], ["blah", "blah"]]}/>
				{:else if visible_array[1]}
					<Chatbox name={arrayOfNames[1]} resetfn={toggleReset} messages={[["j", "w"], ["b", "b"]]}/>
				{:else if visible_array[2]}
					<Chatbox name={arrayOfNames[2]} resetfn={toggleReset} messages={[["joel", "tan"], ["jun", "yao"]]}/>
				{:else}
					<div>
						<div>
							<h3>
							Round: {round}, Room: A
						</h3>
						</div>
						<div>
						<Othercardplatter fn1={toggleVisible1} fn2={toggleVisible2} fn3={toggleVisible3} namesList={arrayOfNames.slice(0, 3)}/>
						</div>
						<div>
						<CardSpecial role={rowdict[role]} name={"You"} />
						</div>
						<div><button on:click={goToVote}>Vote</button></div>
						<div><button on:click={nextRound}>Next Round</button></div>
					</div>
					
					
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
		align-items: center;
		flex: auto;
	}

	h1 {
		width: 100%;
	}

	h3 {
		color: white;
	}

</style>
