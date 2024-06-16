CSS STD:
```css
body {
    display: grid;
    grid-template-areas: 
        "header header header"
        "aside_left main aside_right"
        "footer footer footer";
    grid-template-rows: 1fr 8fr 1fr;
    grid-template-columns: 0.5fr 9fr 0.5fr;
    height: 100vh;
}

.header {
    grid-area: header;

    background-color: blue;
}

.aside {
    background-color: green;
}

.aside_left {
    grid-area: aside_left;
}

.aside_right {
    grid-area: aside_right;
}

.main {
    grid-area: main;

    background-color: red;
}
    
.footer {
    grid-area: footer;

    background-color: yellow;
}

```