
function getStorage(key: string) {
    return localStorage.getItem(key)
}

function removeStorage(key: string) {
    localStorage.removeItem(key)
}

function setStorage(key: string, value: string) {
    localStorage.setItem(key, value)
}

export { getStorage, removeStorage, setStorage }