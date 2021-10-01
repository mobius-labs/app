<template>
    <div>
        <section class="section">
            <div class="container">
                <h1 class="title">Error 404</h1>
                <p class="subtitle">
                    Oh no! The page you were trying to reach was not found.
                </p>
                <p>
                    <router-link class="button" to="/">
                        Go back to home
                    </router-link>
                </p>
            </div>
        </section>
    </div>
</template>

<script>
export default {
    name: "PageNotFound",
};
</script>

<style scoped></style>
