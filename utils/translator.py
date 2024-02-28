import argostranslate.package
import argostranslate.translate

def install_translator_packages():
    from_code = "pt"
    to_code = "en"

    argostranslate.package.update_package_index()
    available_packages = argostranslate.package.get_available_packages()
    available_package = list(
        filter(
            lambda x: x.from_code == from_code and x.to_code == to_code, available_packages
        )
    )[0]
    download_path = available_package.download()
    argostranslate.package.install_from_path(download_path)

def traduz_texto_2(texto_portugues, translation):
    # Traduz texto
    texto_ingles = translation.translate(texto_portugues)
    return texto_ingles

def configura_traducao():
    from_code = "pt"
    to_code = "en"

    installed_languages = argostranslate.translate.get_installed_languages()
    from_lang = next((lang for lang in installed_languages if lang.code == from_code), None)
    to_lang = next((lang for lang in installed_languages if lang.code == to_code), None)

    # Criar objeto de tradução
    translation = from_lang.get_translation(to_lang)

    return translation

def traduz_texto(texto_portugues):
    
    translation = configura_traducao()

    # Traduzir texto
    texto_ingles = translation.translate(texto_portugues)
    
    return texto_ingles


def traduz_lista(lista_portugues):

    translation = configura_traducao()
    lista_ingles = []

    # Traduzir texto
    for frase_portugues in lista_portugues:
        frase_ingles = translation.translate(frase_portugues)
        lista_ingles.append(frase_ingles)
    
    return lista_ingles
