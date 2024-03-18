document.addEventListener('DOMContentLoaded', function() {
	const chapterBookBtn = document.getElementById("chapter_book_btn");
	const createBookBtn = document.getElementById("create_book_btn");



	chapterBookBtn.addEventListener("click", function(e) {
		e.preventDefault();
		const table = document.getElementById('chapter_table').getElementsByTagName('tbody')[0];
		const newRow = table.insertRow();
		const numCells = 6;
		for (let i = 0; i < numCells; i++) {
			const newCell = newRow.insertCell(i);
			var input = document.createElement("input");
			input.type = "text";
			input.className = "form-input";

			input.style.width = "100%";
			input.style.textAlign = "center";
			newCell.appendChild(input)
		}
	});


	createBookBtn.addEventListener("click", function(e) {
		e.preventDefault();
		var bookObject = {};
		var table_contents = [];

		var title = document.getElementById("title").value;
		var author = document.getElementById("author").value;
		var isbn = document.getElementById("isbn").value;
		var book_cover_image = document.getElementById("book_cover_image").value;
		var total_pages = parseInt(document.getElementById("total_pages").value);
		var total_locations = parseInt(document.getElementById("total_locations").value);
		var is_ebook = document.getElementById("is_ebook").value.toLowerCase() === "true" ? true : false;
		var word_count_aprox = parseInt(document.getElementById("word_count_aprox").value);
		var location_to_page = parseFloat(document.getElementById("location_to_page").value);
		var tbody = document.getElementById("table_body");
		var tbodyArr = Array.from(tbody.children);

		tbodyArr.forEach((tbody) => {
			var tempObject = {
				"title": tbody.children[0].children[0].value,
				"order": parseInt(tbody.children[1].children[0].value),
				"ebook": {
					"location_start": parseInt(tbody.children[2].children[0].value),
					"location_end": parseInt(tbody.children[3].children[0].value)
				},
				"printed": {
					"page_start": parseInt(tbody.children[4].children[0].value),
					"page_end": parseInt(tbody.children[5].children[0].value)
				}
			};

			table_contents.push(tempObject);
		});

		bookObject = { title, author, isbn, book_cover_image, total_pages, total_locations, is_ebook, word_count_aprox, location_to_page, table_contents };

		sendPostRequest(bookObject);
	});

	function sendPostRequest(body) {
		fetch('/v1/api/books', {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify(body)
		})
			.then(response => response.json())
			.then(data => {
				console.log(data);
				location.reload(true);
			})
			.catch(error => console.error('Error:', error));

	}

});
