

function box(appname, appurl, description) {

    const appbox =     <a href={appurl} class='app'>
    <p>{String(appname)}</p>
    <div>
      <div class="description">{description}</div>
    </div>
  </a>
    return(appbox)
}

export { box };


