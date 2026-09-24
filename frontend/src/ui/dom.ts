



//children of elements in the end it will be "massive"
export type ElementChildren = (string | HTMLElement)[];


//interface - instruction like stickers put on paper
export interface ElementAttrs {
    [key: string]: string | EventListener | boolean | undefined;
}

export function createElement(
    tag: string,
    attrs: ElementAttrs = {},
    children: ElementChildren = []
): HTMLElement {

    const el = document.createElement(tag);

    for (const [key, value] of Object.entries(attrs)) {

        if (value === undefined) {
            continue;
    }

    if (key.startsWith("on")) {
        if (typeof value === "function") {
        const eventName = key.slice(2).toLowerCase();
        el.addEventListener(eventName, value as EventListener);
    } else {
        console.warn(`Security Error: atribute ${key} must be a function, but not a ${typeof value}`);
        continue;
        }
    }
    
    else if (typeof value === "boolean") {
       if (value === true) {
            el.setAttribute(key, "");
       } else {
            el.removeAttribute(key);
       }
         
    } else {
        el.setAttribute(key, String(value));
    }
}


    for (const child of children) {

        if (typeof child === "string") {
            const textNode = document.createTextNode(child);
            el.appendChild(textNode);
        } else {
            el.appendChild(child);
        }

    }

    return el;
}