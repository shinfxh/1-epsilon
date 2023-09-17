<script>
	import Counter from './Counter.svelte';
	import Role from './Role.svelte';
	import Event from './Event.svelte';
	import Card from './Card.svelte';
	import CardSpecial from './CardSpecial.svelte';
	import Chatbox from './Chatbox.svelte';
	import Roundcounter from './Roundcounter.svelte';
	import Othercard from './Othercard.svelte';
	import ResultPage from './ResultPage.svelte';
	import Othercardplatter from './Othercardplatter.svelte';
	import Othercardplattervote from './Othercardplattervote.svelte';
	import Welcome from './Welcome.svelte';
	import welcome from '$lib/images/svelte-welcome.webp';
	import welcome_fallback from '$lib/images/svelte-welcome.png';

    import { onMount } from 'svelte';
	let role = 0;
	let round = 1;
	let room = 'A';
	let otherroom = 'B';

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
	let aha1 = "";
	let aha2 = "";
	let aha3 = "";

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
	async function toggleVisible1(){
		visible_array[0] = !visible_array[0];
		visible_array[1] = 0;
		visible_array[2] = 0;
		fetch('http://localhost:5000/getMessages?p1=Player&p2=' + aha1)
		.then((response) => response.json())
		.then((data) => {
			console.log(data);
			messages1 = data;
		});
	}

	async function refresh1(){
		fetch('http://localhost:5000/getMessages?p1=Player&p2=' + aha1)
		.then((response) => response.json())
		.then((data) => {
			console.log(data);
			messages1 = data;
		});
	}
	async function toggleVisible2(){
		visible_array[0] = 0;
		visible_array[1] = !visible_array[1];
		visible_array[2] = 0;
		fetch('http://localhost:5000/getMessages?p1=Player&p2=' + aha2)
		.then((response) => response.json())
		.then((data) => {
			console.log(data);
			messages1 = data;
		});
	}
	async function refresh2(){
		fetch('http://localhost:5000/getMessages?p1=Player&p2=' + aha2)
		.then((response) => response.json())
		.then((data) => {
			console.log(data);
			messages2 = data;
		});
	}
	async function toggleVisible3(){
		visible_array[0] = 0;
		visible_array[1] = 0;
		visible_array[2] = !visible_array[2];
		fetch('http://localhost:5000/getMessages?p1=Player&p2=' + aha3)
		.then((response) => response.json())
		.then((data) => {
			console.log(data);
			messages1 = data;
		});
	}
	async function refresh3(){
		fetch('http://localhost:5000/getMessages?p1=Player&p2=' + aha3)
		.then((response) => response.json())
		.then((data) => {
			console.log(data);
			messages3 = data;
		});
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
	// 5: END

	let messages1 = [];
	let messages2 = [];
	let messages3 = [];
	let eventStr = "";
	let resultStr = "The End";

	// voting mechanism
	function votedEventStr(i){
		let returnStr = "Player voted " + arrayOfNames[i] + ";";
		let arr = [0, 0, 0, 0];
		arr[i] += 1;
		for (var i = 0; i < 3; i++){
			let x = getRandomInt(4);
			arr[x] += 1;
			if (x == 3){
				returnStr += arrayOfNames[i] + " voted Player"+ ";";
			} else {
				returnStr += arrayOfNames[i] + " voted " + arrayOfNames[x] + ";";
			}
		}
		let curmax = -1;
		let curidx = -1;
		let neq = 0;
		for (var i = 0; i < 4; i++){
			if (arr[i] > curmax){
				curmax = arr[i];
				curidx = i;
				neq = 1;
			} else if (arr[i] == curmax){
				neq += 1;
				// swap index with 1/neq probability
				let x = getRandomInt(neq);
				if (x == 0){
					curidx = i;
				}
			}
		}
		if (curidx == 3){
			returnStr += "Player was voted to go to the other room.;"
			let randidx = 3 + getRandomInt(4);
			returnStr += arrayOfNames[randidx] + " was voted to come into the room."
			// choose one person to swap
			const temper = arrayOfNames[randidx];
			arrayOfNames[randidx] = arrayOfNames[3];
			arrayOfNames[3] = temper;

			arrayOfNames = arrayOfNames.reverse();
			
			// swap rooms
			let temp = otherroom;
			otherroom = room;
			room = temp;

			aha1 = arrayOfNames[0];
			aha2 = arrayOfNames[1];
			aha3 = arrayOfNames[2];
			console.log("aha1 = ", aha1, "aha2 = ", aha2, "aha3 = ", aha3, "temper = ", temper);
		} else {
			returnStr += arrayOfNames[curidx] + " was voted to go to the other room.;"
			let randidx = 3 + getRandomInt(4);
			returnStr += arrayOfNames[randidx] + " was voted to come into the room."

			// choose one person to swap
			const temper = arrayOfNames[randidx];
			arrayOfNames[curidx] = arrayOfNames[randidx];
			arrayOfNames[randidx] = temper;
			aha1 = arrayOfNames[0];
			aha2 = arrayOfNames[1];
			aha3 = arrayOfNames[2];
			console.log("aha1 = ", aha1, "aha2 = ", aha2, "aha3 = ", aha3, "temper = ", temper);
		}
		eventStr = returnStr;
		return returnStr;
	}

	function toggleState(newState){
		if (state == 0){
			role = getRandomInt(8);
			arrayOfNames = shuffle(arrayOfNames);
			aha1 = arrayOfNames[0];
			aha2 = arrayOfNames[1];
			aha3 = arrayOfNames[2];
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
		<Event eventNo={1} eventStr={eventStr}/>
		<button on:click={()=>{if (round < 3){toggleState(1);} else {toggleState(5);}}}>Ok, noted.</button>
	{:else if state == 5}
		<ResultPage eventStr={resultStr}/>
	
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
						Round: {round}, Room: {room}
						<br>
						Vote for a player to go to Room {otherroom}
						</h3>
					</div>
				<div style="width:100%; color:red;">
				<Othercardplattervote fn1={()=>{votedEventStr(0);toggleState(4);round+=1;}} fn2={()=>{votedEventStr(1);toggleState(4);round+=1;}} fn3={()=>{votedEventStr(2);toggleState(4);round+=1;}} namesList={[aha1, aha2, aha3]}/>
				</div>
				<div>
				<CardSpecial role={rowdict[role]} name={"Player"} />
				</div>
				</div>

			{:else}

				{#if visible_array[0]}
					<Chatbox name={aha1} resetfn={toggleReset} messages={messages1} refresh={refresh1}/>
				{:else if visible_array[1]}
					<Chatbox name={aha2} resetfn={toggleReset} messages={messages2} refresh={refresh2}/>
				{:else if visible_array[2]}
					<Chatbox name={aha3} resetfn={toggleReset} messages={messages3} refresh={refresh3}/>
				{:else}
					<div>
						<div>
							<h3>
							Round: {round}, Room: {room}
						</h3>
						</div>
						<div>
						<Othercardplatter fn1={toggleVisible1} fn2={toggleVisible2} fn3={toggleVisible3} namesList={[aha1, aha2, aha3]}/>
						</div>
						<div>
						<CardSpecial role={rowdict[role]} name={"You"} />
						</div>
						<div><button on:click={() => toggleState(3)}>Vote</button></div>
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
