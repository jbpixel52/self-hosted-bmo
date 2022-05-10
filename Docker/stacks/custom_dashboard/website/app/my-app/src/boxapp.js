function box(appname, appurl,description) {
    return(
        <a href={appurl}>{appname}
            <div class='app'>
            <div class='description'>{description}</div>
            </div>
        </a>
    )
}


export {box}