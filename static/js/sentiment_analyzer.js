document.addEventListener('DOMContentLoaded', () => {
    const tabs = document.querySelectorAll('.tabs li');
    const tabContentBoxes = document.querySelectorAll('#tab-content .tab-content');

    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            tabs.forEach(item => item.classList.remove('is-active'));
            tab.classList.add('is-active');

            const target = tab.dataset.tab;
            tabContentBoxes.forEach(box => {
                if (box.getAttribute('id') === target) {
                    box.classList.add('is-active');
                } else {
                    box.classList.remove('is-active');
                }
            });
        });
    });
});

function enviarTexto() {
    var textoParaEnviar = $('#input_text').val();

    $.ajax({
        url: "http://127.0.0.1:5000/sentiment_analyzer_text",
        type: "POST",
        data: textoParaEnviar,
        contentType: "text/plain; charset=utf-8",
        success: function(data, status) {
            console.log("Resposta recebida: ", data);
            // alert("Texto enviado com sucesso!");
            // Acessando cada propriedade do objeto JSON
            var classificacao = data["Classificacao do Sentimento"];
            var textoOriginal = data["Texto Original"];
            var textoTratado = data["Texto apos o tratamento"];
            var cor = "gray"
            if(classificacao=="Positivo"){
                cor = "green"
            }
            else if(classificacao=="Negativo"){
                cor = "red"
            }
            limpa_retorno_texto()
            var div_resposta = document.getElementById("container_resposta");
            div_resposta.innerHTML += '<p><strong>Classificação do Sentimento: </strong><strong style="color:'+cor+'">'+classificacao+'</strong></p><p><strong>Texto Original: </strong>'+textoOriginal+'</p><p><strong>Texto após o tratamento: </strong>'+textoTratado+'</p>'
        },
        error: function(xhr, status, error) {
            alert("Erro ao enviar o texto: " + error);
        }
    });
}

function limpa_retorno_texto(){
    var div_resposta = document.getElementById("container_resposta");
    div_resposta.innerHTML = ""

}

function enviarArquivo() {
    // Captura o arquivo do input
    var arquivo = $('#inputGroupFile04').prop('files')[0];
    var nomeDoArquivo = arquivo.name;

    if (!arquivo) {
      alert('Por favor, selecione um arquivo CSV para enviar.');
      return;
    }
  
    // Cria um FormData e adiciona o arquivo
    // var formData = new FormData();
    // formData.append('file', arquivo);

    var separador = document.getElementById("separador").value;
    var nome_coluna_texto = document.getElementById("nome_coluna_texto").value;

    // Chama a API Flask usando jQuery.ajax
    $.ajax({
      url: 'http://127.0.0.1:5000/sentiment_analyzer_csv/'+nome_coluna_texto+'/'+separador, // Substitua pela URL da sua API Flask
      type: 'POST',
      data: arquivo,
      contentType: 'text/csv', // Define o tipo de conteúdo como text/csv
      processData: false, // Impede o jQuery de processar os dados
    //   contentType: false, // Impede o jQuery de definir o tipo de conteúdo
      success: function(response) {
        // Cria um Blob a partir da resposta, assumindo que 'response' é uma string CSV
        var blob = new Blob([response], { type: 'text/csv;charset=utf-8;' });
      
        // Cria um URL para o Blob
        var downloadUrl = URL.createObjectURL(blob);
      
        // Cria um elemento de link temporário programaticamente
        var downloadLink = document.createElement("a");
        document.body.appendChild(downloadLink); // Necessário para que o Firefox processe o clique
      
        downloadLink.href = downloadUrl;
        downloadLink.download = "output_"+nomeDoArquivo; // Define o nome do arquivo para o download
        downloadLink.click(); // Simula um clique no link de download
      
        document.body.removeChild(downloadLink); // Remove o link da página
        URL.revokeObjectURL(downloadUrl); // Libera o URL do Blob
      
        alert('Arquivo baixado com sucesso!');
      },      
      error: function(xhr, status, error) {
        console.error(error); // Trata erros na requisição
        alert('Erro ao enviar arquivo: ' + error);
      }
    });
  }
  