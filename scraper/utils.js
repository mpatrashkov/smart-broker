async function getPhoneFromElement(element) {
    const onclick = element.attribs.onclick
    const open_contact_code = onclick.split("'")[1]
    const data =
        "open_contact=" +
        encodeURIComponent(open_contact_code) +
        "&step=" +
        encodeURIComponent("request") +
        "&data=" +
        encodeURIComponent("")

    const response = await axios.post(example_url + "?force_session=1", data)

    const regex_search = response.data.match(regex_tel)
    return regex_search[1]
}

function getPhotoUrls(html_text) {
    const urls = []
    const regex_matches = html_text.match(regex_photos)
    regex_matches.map((match) => urls.push(base_url + match))
    return urls
}

module.exports = { getPhotoUrls, getPhoneFromElement }
