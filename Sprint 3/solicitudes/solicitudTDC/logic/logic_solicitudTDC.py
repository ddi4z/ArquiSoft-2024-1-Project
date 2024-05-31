from tarjetasDisponibles.models import TarjetaDisponible

def init_globals():
    tarjetasDisponibles = [
        {
            'perfil': 'Classic',
            'franquicia': 'VISA',
            'imagen': 'https://www.visa.com.co/dam/VCOM/regional/lac/SPA/Default/Pay%20With%20Visa/Find%20a%20Card/Credit%20cards/Classic/visa_classic_card_400x225.jpg',
            'descripcion': 'Tarjeta de crédito Classic VISA',
            'tiempoVigenciaMeses': 36
        },
        {
            'perfil': 'Gold',
            'franquicia': 'VISA',
            'imagen': 'https://www.visa.com.co/dam/VCOM/regional/lac/SPA/Default/Pay%20With%20Visa/Find%20a%20Card/Credit%20cards/Gold/visa_gold_card_400x225.jpg',
            'descripcion': 'Tarjeta de crédito Gold VISA',
            'tiempoVigenciaMeses': 36
        },
        {
            'perfil': 'Platinum',
            'franquicia': 'VISA',
            'imagen': 'https://www.visa.com.co/dam/VCOM/regional/lac/SPA/Default/Pay%20With%20Visa/Tarjetas/visa-platinum-400x225.jpg',
            'descripcion': 'Tarjeta de crédito Platinum VISA',
            'tiempoVigenciaMeses': 36
        },
        {
            'perfil': 'Signature',
            'franquicia': 'VISA',
            'imagen': 'https://www.visa.com.co/dam/VCOM/regional/lac/SPA/Default/Pay%20With%20Visa/Tarjetas/visa-signature-400x225.jpg',
            'descripcion': 'Tarjeta de crédito Signature VISA',
            'tiempoVigenciaMeses': 36
        },
        {
            'perfil': 'Standard',
            'franquicia': 'MasterCard',
            'imagen': 'https://www.mastercard.com.co/content/dam/public/mastercardcom/lac/mx/home/consumidores/encontrar-una-tarjeta/tarjetas-de-credito/tarjeta-standard/tarjeta-credito-standard-1280x720.jpg',
            'descripcion': 'Tarjeta de crédito Standard MasterCard',
            'tiempoVigenciaMeses': 36
        },
        {
            'perfil': 'Gold',
            'franquicia': 'MasterCard',
            'imagen': 'https://www.mastercard.com.pe/content/dam/public/mastercardcom/lac/mx/home/consumidores/encontrar-una-tarjeta/tarjetas-de-credito/tarjeta-gold/tarjeta-credito-gold-1280x720.jpg',
            'descripcion': 'Tarjeta de crédito Gold MasterCard',
            'tiempoVigenciaMeses': 36
        },
        {
            'perfil': 'Platinum',
            'franquicia': 'MasterCard',
            'imagen': 'https://www.mastercard.com.co/content/dam/public/mastercardcom/lac/mx/home/consumidores/encontrar-una-tarjeta/tarjetas-de-credito/tarjeta-platinum/tarjeta-credito-platinum-1280x720.jpg',
            'descripcion': 'Tarjeta de crédito Platinum MasterCard',
            'tiempoVigenciaMeses': 36
        },
        {
            'perfil': 'Black',
            'franquicia': 'MasterCard',
            'imagen': 'https://www.mastercard.cl/content/dam/public/mastercardcom/lac/co/home/consumidores/encuentra-tu-tarjeta/tarjetas-de-credito/tarjeta-black/tarjeta-black-credito-1280x720.jpg',
            'descripcion': 'Tarjeta de crédito Black MasterCard',
            'tiempoVigenciaMeses': 36
        }
    ]

    for tarjeta in tarjetasDisponibles:
        TarjetaDisponible.objects.get_or_create(
            perfil=tarjeta['perfil'],
            franquicia=tarjeta['franquicia'],
            imagen=tarjeta['imagen'],
            descripcion=tarjeta['descripcion'],
            tiempoVigenciaMeses=tarjeta['tiempoVigenciaMeses']
        )