<script>
	export let eventStr;
	let array = eventStr.split(";");
</script>

<div class="resultpage">
	{#each array as el, idx}
		<h3>{el}</h3>
	{/each}
</div>

<style>

	h3 {
		color:white;
	}

</style>
