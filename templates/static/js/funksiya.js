
export const addRow = async (dataTable, item) => {

    const myModalEl = document.getElementById('exampleModal');
    const modal = bootstrap.Modal.getInstance(myModalEl)

    delete item.id

    // server
    fetch (`telefon/add/`, {
        method: "POST",
        body: JSON.stringify(item),
    })
        .then((response) => {
            if(!response.ok) {
                return response.text().then(text => { throw new Error(text) })
            } else {
                return response.json()
            }
        })
        .then((result) => {
            dataTable.rows().add(
                [...Object.values({id: result.id.toString(),...item}),editBtn + " " + removeBtn]
            )

            const alert = document.querySelector('.alert')
            alert.className = alert.className.replace('d-block','d-none')
            location.reload();

            modal.hide();
        })
        .catch((err) => {
            const alert = document.querySelector('.alert')
            alert.textContent = JSON.parse(err.toString().replace('Error: ','')).detail
            alert.className = alert.className.replace('d-none','d-block')
        })
}

export const editRow = (dataTable , item) => {

    const id = item.id
    delete item.id

    // server
    fetch (`/telefon/edit/${id}/`, {
        method: "POST",
        body: JSON.stringify(item),
    })
        .then((response) => {
            if(!response.ok) {
                return response.text().then(text => { throw new Error(text) })
            } else {
                return response.json()
            }
        })
        .then((result) => {

            dataTable.data.forEach((d,i) => {
                if ( dataTable.data[i].cells[0].data === item.id ) {
                    dataTable.rows().remove(i)
                }
            })
            dataTable.rows().add(
                [...Object.values(item),editBtn + " " + removeBtn]
            )

            const alert = document.querySelector('.alert')
            alert.className = alert.className.replace('d-block','d-none')
            location.reload();
        })
        .catch((err) => {
            const alert = document.querySelector('.alert')
            alert.textContent = JSON.parse(err.toString().replace('Error: ','')).detail
            alert.className = alert.className.replace('d-none','d-block')
        })
}

export const removeRow = (dataTable , item) => {

    const id = dataTable.data[item].cells[0].data

    // server
    fetch (`/telefon/delete/${id}/`, {
        method: "POST",
    })
        .then((response) => {
            if(!response.ok) {
                return response.text().then(text => { throw new Error(text) })
            } else {
                return response.json()
            }
        })
        .then((result) => {
            dataTable.rows().remove(item)

            setToastBody(result.message,'success')
            toast.show()
            location.reload()
     })
        .catch((err) => {
            setToastBody(JSON.parse(err.toString().replace('Error: ','')).detail,'fail')
            toast.show()
        })

}
