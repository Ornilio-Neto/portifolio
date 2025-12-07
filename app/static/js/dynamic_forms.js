document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.dynamic-section').forEach(section => {
        const prefix = section.dataset.prefix;
        const list = section.querySelector('.dynamic-list');
        const addButton = section.querySelector('.add-item-btn');
        const template = document.getElementById(`${prefix}-template`);

        // Inicia o contador com o número de itens já renderizados pelo servidor
        let count = list.children.length;

        addButton.addEventListener('click', () => {
            // Clona o conteúdo do molde
            const clone = template.content.cloneNode(true);

            // Substitui o placeholder __prefix__ nos atributos `name`, `id`, e `for`
            clone.querySelectorAll('[name], [id], label[for]').forEach(el => {
                if (el.name) {
                    el.name = el.name.replace('__prefix__', count);
                }
                if (el.id) {
                    el.id = el.id.replace('__prefix__', count);
                }
                if (el.htmlFor) {
                    el.htmlFor = el.htmlFor.replace('__prefix__', count);
                }
            });

            list.appendChild(clone);
            count++; // Incrementa o contador para o próximo item
        });

        // Delegação de evento para o botão de remover
        list.addEventListener('click', e => {
            if (e.target && e.target.classList.contains('remove-item-btn')) {
                e.target.closest('.dynamic-item').remove();
            }
        });
    });
});
