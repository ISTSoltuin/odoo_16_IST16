/** @odoo-module **/

odoo.define('fandi_api_integration.simulador_financiamento', function (require) {
    "use strict";

    const VariantMixin = require('website_sale.VariantMixin');
    const originalOnChangeCombination = VariantMixin._onChangeCombination;
    const rpc = require('web.rpc');

    VariantMixin._onChangeCombination = function (ev, $parent, combination) {
        // Lógica original
        originalOnChangeCombination.apply(this, [ev, $parent, combination]);

        // Adiciona comportamento para o botão "Simule"
        const simulateWrap = $parent.find('#simulate_wrap');
        const formContainer = $parent.find('#formSimulacaoContainer');

        if (combination.is_combination_possible) {
            simulateWrap.removeClass('d-none').addClass('d-inline-flex');
        } else {
            simulateWrap.removeClass('d-inline-flex').addClass('d-none');
            formContainer.hide(); // Oculta o formulário se a combinação for inválida
        }
    };

    // Captura o clique no botão "Simule"
    $(document).on('click', '#simulate_button', function (e) {
        e.preventDefault();

        const formContainer = $('#formSimulacaoContainer');
        if (formContainer.is(':visible')) {
            formContainer.fadeOut();
        } else {
            formContainer.fadeIn();
        }
    });
    
    $(document).on('click', '#btnSimular', async function (e) {
        e.preventDefault();

        const formContainer = $('#formSimulacaoContainer');
        const name = $('#name').val();
        const cpf = $('#cpf').val();
        const telefone = $('#telefone').val();
        const productId = parseInt(document.documentElement.getAttribute('data-main-object').match(/\((\d+),\)/)?.[1]);

        // chamar rota da api /simulador/enviar
        // Chamada para a API utilizando rpc.query, com sudo ativado
        await rpc.query({
            route: '/simulador/enviar',
            params: {
                'name': name,
                'cpf': cpf,
                'telefone': telefone,
                'product_id': productId
            }
        }).then(function (response) {
            if (response.success) {
                // Atualizar o frontend com o resultado da simulação
                // alert(`Simulação realizada com sucesso!\nParcelas: ${response.parcelas}\nValor por parcela: ${response.valor_parcela}`);
                const resultContainer = $('#resultadoSimulacao');
                if (resultContainer.is(':visible')) {
                    resultContainer.fadeOut();
                } else {
                    resultContainer.find('#parcelas').text(response.quantidade_parcelas);
                    resultContainer.find('#valorParcela').text(response.valor_parcela);
                    resultContainer.find('#percentualEntrada').text(response.valor_entrada);
                    resultContainer.find('#valorVeiculo').text(response.valor_veiculo);
                    // resultContainer.find('#valorEntrada').text(response.valor_entrada);

                    let linkRedirecionamento = response.link_redirecionamento;
                    // Se o link não começa com "http" ou "https", forçamos o formato correto
                    if (!linkRedirecionamento.startsWith('http')) {
                        linkRedirecionamento = `https://wa.me/${linkRedirecionamento.replace(/[^0-9]/g, '')}`;
                    }
                    resultContainer.find('#linkRedirecionamento').html(
                        `<a href="${linkRedirecionamento}" target="_blank" style="color: #fff;">Entre em Contato Conosco</a>`
                    );
                    formContainer.fadeOut();
                    resultContainer.fadeIn();
                    return response
                }
            } else {
                alert(`Erro: ${response.message}`);
            }
        });
    });

    return VariantMixin;
});
