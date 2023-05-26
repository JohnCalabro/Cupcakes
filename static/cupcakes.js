

function make_cupcake_html(cupcake) {
    return `
    <div data-cupcake-id=${cupcake.id}>
      <li>
        ${cupcake.flavor} / ${cupcake.size} / ${cupcake.rating}
        <button class="delete-button">X</button>
      </li>
      <img class="Cupcake-img"
            src="${cupcake.image}"
            alt="(no image provided)">
    </div>
  `;
}

async function put_cakes_on_page() {
    const res = await axios.get('http://127.0.0.1:5000/api/cupcakes');
    console.log(res)
    for (let cake of res.data.cupcakes) {
      let newCake = $(make_cupcake_html(cake));
      $("#list").append(newCake);
    }
  }
  


  $("#new-cupcake-form").on("submit", async function (evt) {
    evt.preventDefault();
  
    let flavor = $("#form-flavor").val();
    let rating = $("#form-rating").val();
    let size = $("#form-size").val();
    let image = $("#form-image").val();
  
    const newCupcakeResponse = await axios.post('http://127.0.0.1:5000/api/cupcakes', {
      flavor,
      rating,
      size,
      image
    });
  
    let newCupcake = $(make_cupcake_html(newCupcakeResponse.data.cupcake));
    $("#list").append(newCupcake);
    $("#new-cupcake-form").trigger("reset");
  });

  $("#list").on("click", ".delete-button", async function (evt) {
    evt.preventDefault();
    let $cupcake = $(evt.target).closest("div");
    let cupcakeId = $cupcake.attr("data-cupcake-id");
  
    await axios.delete(`http://127.0.0.1:5000/api/cupcakes/${cupcakeId}`);
    $cupcake.remove();
  });

  $(put_cakes_on_page);