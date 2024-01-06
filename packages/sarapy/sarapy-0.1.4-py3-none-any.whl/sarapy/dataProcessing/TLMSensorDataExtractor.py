"""
La clase MetadataManager se encarga de gestionar los metadatos obtenidos de la base de datos. Estos metadatos se corresponden con los datos registrados en los sarapicos.

- Versión de metadatos utilizada: Revision 9
- Apuntes de identificiación: https://docs.google.com/document/d/1E-TvkMWqeL9d57FOeRH7Zk_Fr5SdmknnmuQ7n7uwUVg/edit#heading=h.3dy6vkm
- Apuntes de
- Apuntes de Desarrollo: 

- Autor: BALDEZZARI Lucas
"""

##importamos numpy
import numpy as np
# from geopy.distance import geodesic

from sklearn.base import BaseEstimator, TransformerMixin

class TLMSensorDataExtractor(BaseEstimator, TransformerMixin):
    """
    Clase que se encarga de procesar los metadatos obtenidos de la base de datos histórica.

    - Versión de metadatos utilizada: Revision 9 
    - Link documento metadato: https://trello.com/c/M6DWjpwr/70-definici%C3%B3n-metadatos-a-relevar
    - Los metadatos de DATA_TLM en la Revisión 9 vienen en un string de 0 y 1. Estos valores indican, lo siguiente:
    |RF(1bit)|GNSS(1bit)|RFID(1bit)|FLASH(1bit)|RTCS(1bit)|MODE(1bit)|NBAT(2bits)|TIMEAC(8bits)|ESTAC(1bit)|DSTR PT(4bits)|INEST PT(1bit)|OFFS PT(2bits)|X(1bit)|DSTR FT(4bits)|INEST FT(1bit)|OFFS FT(2bits)|X(1bit)|GYRO_X(3bits)|GYRO_Y(3bits)|GYRO_Z(2bits)|ACEL_X(2bits)|ACEL_Y(2bits)|ACEL_Z(2bits)|EST MO(1bit)|EST OR(1bit)|SBAT(2bits)|VBAT(3bits)|CBAT(2bits)|EST BMS(1bit)
    
    Los valores X indican bit sin uso.

    - Versión 1.0.0.RevA
    - Autor: BALDEZZARI Lucas
    """
    
    __metadataVersion = "Revision 9" #Versión de metadatos utilizada

    def __init__(self, *args, **kwargs):
        """
        Constructor de la clase MetadataManager.

        :param metadata: Diccionario con los metadatos obtenidos de la base de datos.
        :type metadata: strg
        """

        ### Creamos constantes que sirven para buscar los datos en el string de telemetría
        ### Cada constante es una tupla con la posición del bit menos significativo y la posición del bit más significativo
        self.__RFflag_pos = (0,0) #RF(1bit)
        self.__GNSSflag_pos = (1,1) #GNSS(1bit)
        self.__RFIDflag_pos = (2,2) #RFID(1bit)
        self.__FLASHflag_pos = (3,3) #FLASH(1bit)
        self.__RTCSflag_pos = (4,4) #RTCS(1bit)
        self.__MODEflag_pos = (5,5) #MODE(1bit)
        self.__NBAT_pos = (6,7) #NBAT(2bits)
        self.__TIMEAC_pos = (8,14) #TIMEAC(8bits)
        self.__ESTACflag_pos = (15,15) #ESTAC(1bit)
        self.__DSTRPT_pos = (16,19) #DSTR PT(4bits)
        self.__INESTPTflag_pos = (20,20) #INEST PT(1bit) Inestabilidad de plantín
        self.__OFFSPT_pos = (21,22) #OFFS PT(2bits)
        self.__DSTRFT_pos = (24,27) #DSTR FT(4bits)
        self.__INESTFTflag_pos = (28,28) #INEST FT(1bit)
        self.__OFFSFT_pos = (29,30) #OFFS FT(2bits)
        self.__PMSTFlag = (31,31) #PMST(1bit)
        self.__GYROX_pos = (32,34) #GYRO_X(3bits)
        self.__GYROY_pos = (35,37) #GYRO_Y(3bits)
        self.__GYROZf_pos = (38,39) #GYRO_Z(2bits)
        self.__ACELX_pos = (40,41) #ACEL_X(2bits)
        self.__ACELY_pos = (42,43) #ACEL_Y(2bits)
        self.__ACELZ_pos = (44,45) #ACEL_Z(2bits)
        self.__ESTMOflag_pos = (46,46) #EST MO(1bit)
        self.__ESTORflag_pos = (47,47) #EST OR(1bit)
        self.__SBAT_pos = (48,49) #SBAT(2bits) salud de la batería
        self.__VBAT_pos = (50,52) #VBAT(3bits) voltaje de la batería
        self.__CBAT_pos = (53,54) #CBAT(2bits) consumo de la batería
        self.__ESTBMSflag_pos = (55,55) #EST BMS(1bit)
        
        # self.kilometers = kwargs.pop('kilometers', 0)
        self.is_fitted = False

    def fit(self, X, y=None):
        """
        Método para generar datos a partir de la metadata.

        X es un array de strings. Cada string es un dato de la metadata.

        Extraigo información de cada fila de X. Genero numpys array de cada dato extraido de la metadata.

        Parametros
        ----------
            X: Array de strings.
            y: None
                No se utiliza.
        """

        ##chequeamos si todos los strings de X tienen la misma longitud, sino arrojamos un assert
        assert all(len(x) == len(X[0]) for x in X), "Todos los strings de X deben tener la misma longitud"

        self.RFFlag = np.vectorize(self.getRFFlag)(X)
        self.GNSSFlag = np.vectorize(self.getGNSSFlag)(X)
        self.RFIDFlag = np.vectorize(self.getRFIDFlag)(X)
        self.FLASHFlag = np.vectorize(self.getFLASHFlag)(X)
        self.RTCSFlag = np.vectorize(self.getRTCSFlag)(X)
        self.MODEFlag = np.vectorize(self.getMODEFlag)(X)
        self.NBAT = np.vectorize(self.getNBAT)(X)
        self.TIMEAC = np.vectorize(self.getTIMEAC)(X)
        self.ESTAC = np.vectorize(self.getESTAC)(X)
        self.DSTRPT = np.vectorize(self.getDSTRPT)(X)
        self.INESTPT = np.vectorize(self.getINESTPTFlag)(X)
        self.OFFSPT = np.vectorize(self.getOFFSPT)(X)
        self.DSTRFT = np.vectorize(self.getDSTRFT)(X)
        self.INESTFT = np.vectorize(self.getINESTFTFlag)(X)
        self.OFFSFT = np.vectorize(self.getOFFSFT)(X)
        self.PMSTFlag = np.vectorize(self.getPMSTFlag)(X)
        self.GYROX = np.vectorize(self.getGYROX)(X)
        self.GYROY = np.vectorize(self.getGYROY)(X)
        self.GYROZ = np.vectorize(self.getGYROZ)(X)
        self.ACELX = np.vectorize(self.getACELX)(X)
        self.ACELY = np.vectorize(self.getACELY)(X)
        self.ACELZ = np.vectorize(self.getACELZ)(X)
        self.ESTMOFlag = np.vectorize(self.getESTMOFlag)(X)
        self.ESTORFlag = np.vectorize(self.getESTORFlag)(X)
        self.SBAT = np.vectorize(self.getSBAT)(X)
        self.VBAT = np.vectorize(self.getVBAT)(X)
        self.CBAT = np.vectorize(self.getCBAT)(X)
        self.ESTBMSFlag = np.vectorize(self.getESTBMSFlag)(X)

        self.is_fitted = True
        

    def transform(self, X, y=None):
        """Genera un array de numpy con los datos extraidos de la metadata.
        
        Forma una matriz de numpy.
        
        Parametros
        ----------
            X: X es un array de strings. Cada string es un dato de la metadata.
            y: None
                No se utiliza."""
        
        ##chequeamos si se ha llamado a fit(). Sino, se arroja un error
        if not self.is_fitted:
            raise ValueError("MetadataManager no ha sido fitteado. Llame a fit() previamente.")
        
        return np.array([   self.RFFlag,
                            self.GNSSFlag,
                            self.RFIDFlag,
                            self.FLASHFlag,
                            self.RTCSFlag,
                            self.MODEFlag,
                            self.NBAT,
                            self.TIMEAC,
                            self.ESTAC,
                            self.DSTRPT,
                            self.INESTPT,
                            self.OFFSPT,
                            self.DSTRFT,
                            self.INESTFT,
                            self.OFFSFT,
                            self.PMSTFlag,
                            self.GYROX,
                            self.GYROY,
                            self.GYROZ,
                            self.ACELX,
                            self.ACELY,
                            self.ACELZ,
                            self.ESTMOFlag,
                            self.ESTORFlag,
                            self.SBAT,
                            self.VBAT,
                            self.CBAT,
                            self.ESTBMSFlag]).T

    def fit_transform(self, X, y=None):
        """Combinamos fit() y transform() en un solo método.
        
        Parametros
        ----------
            X: X es un array de strings. Cada string es un dato de la metadata.
            y: None
                No se utiliza.
        
        Return
        ------
            numpy array:
                Array de numpy con los datos extraidos de la metadata.
                """
        self.fit(X)
        return self.transform(X)

    def getRFFlag(self, metadata):
        """
        Devuelve el valor del flag RF.

        Parametros
        ----------
            metadata: str
                String con los metadatos obtenidos de la base de datos.
        Return
        ------
            int
                Valor del flag RF.
        """

        return np.uint8(int(metadata[self.__RFflag_pos[0]:self.__RFflag_pos[1]+1],2))
    
    def getGNSSFlag(self, metadata):
        """
        Devuelve el valor del flag RF.

        Parametros
        ----------
            metadata: str
                String con los metadatos obtenidos de la base de datos.
        Return
        ------
            int
                Valor del flag GNSS.
        """

        return np.uint8(int(metadata[self.__GNSSflag_pos[0]:self.__GNSSflag_pos[1]+1],2))
    
    def getRFIDFlag(self, metadata):
        """
        Devuelve el valor del flag RFID.

        Parametros
        ----------
            metadata: str
                String con los metadatos obtenidos de la base de datos.
        Return
        ------
            int
                Valor del flag RFID.
        """

        return np.uint8(int(metadata[self.__RFIDflag_pos[0]:self.__RFIDflag_pos[1]+1],2))
    
    def getFLASHFlag(self, metadata):
        """
        Devuelve el valor del flag FLASH.

        Parametros
        ----------
            metadata: str
                String con los metadatos obtenidos de la base de datos.
        Return
        ------
            int
                Valor del flag FLASH.
        """

        return np.uint8(int(metadata[self.__FLASHflag_pos[0]:self.__FLASHflag_pos[1]+1],2))
    
    def getRTCSFlag(self, metadata):
        """
        Devuelve el valor del flag RTCS.

        Parametros
        ----------
            metadata: str
                String con los metadatos obtenidos de la base de datos.
        Return
        ------
            int
                Valor del flag RTCS.
        """

        return np.uint8(int(metadata[self.__RTCSflag_pos[0]:self.__RTCSflag_pos[1]+1],2))
    
    def getMODEFlag(self, metadata):
        """
        Devuelve el valor del flag MODE.

        Parametros
        ----------
            metadata: str
                String con los metadatos obtenidos de la base de datos.
        Return
        ------

            int
                Valor del flag MODE.
        """

        return np.uint8(int(metadata[self.__MODEflag_pos[0]:self.__MODEflag_pos[1]+1],2))
    
    def getNBAT(self, metadata):
        """
        Devuelve el valor del flag NBAT.

        Parametros
        ----------
            metadata: str
                String con los metadatos obtenidos de la base de datos.
        Return
        ------
            int
                Valor del flag NBAT.
        """

        return np.uint8(int(metadata[self.__NBAT_pos[0]:self.__NBAT_pos[1]+1],2))

    def getTIMEAC(self, metadata):
        """
        Devuelve el tiempo de accionamiento en segundos

        Parametros
        ----------
            metadata: str
                String con los metadatos obtenidos de la base de datos.
        Return
        ------
            float
                Tiempo de accionamiento en segundos.
        """

        return np.float16(int(metadata[self.__TIMEAC_pos[0]:self.__TIMEAC_pos[1]+1],2)*0.1)
    
    def getESTAC(self, metadata):
        """
        Devuelve el valor del flag de ANOMALÍA OPERATIVA

        Parametros
        ----------
            metadata: str
                String con los metadatos obtenidos de la base de datos.
        Return
        ------
            int
                Valor del flag de ANOMALÍA OPERATIVA.
        """

        return np.uint8(int(metadata[self.__ESTACflag_pos[0]:self.__ESTACflag_pos[1]+1],2))
    
    def getDSTRPT(self, metadata):
        """
        Devuelve el nivel de distorsión para plantín

        Parametros
        ----------
            metadata: str
                String con los metadatos obtenidos de la base de datos.
        Return
        ------
            int:
                Valor de distorsión para plantín.
        """

        return np.uint8(int(metadata[self.__DSTRPT_pos[0]:self.__DSTRPT_pos[1]+1],2))

    def getINESTPTFlag(self,metadata):
            """
            Devuelve el valor del flag de INESTABILIDAD PARA PLANTÍN

            Parametros
            ----------
                metadata: str
                    String con los metadatos obtenidos de la base de datos.
            Return
            ------
                    int:
                        Valor del flag de INESTABILIDAD PARA PLANTÍN.
            """

            return np.uint8(int(metadata[self.__INESTPTflag_pos[0]:self.__INESTPTflag_pos[1]+1],2))

    def getOFFSPT(self,metadata):
        """
        Devuelve el valor del flag de OFFSET PARA PLANTÍN

        Parametros
        ----------
            metadata: str
                String con los metadatos obtenidos de la base de datos.
        Return
        ------
                int:
                    Valor del flag de OFFSET PARA PLANTÍN.
        """

        return np.uint8(int(metadata[self.__OFFSPT_pos[0]:self.__OFFSPT_pos[1]+1],2))

    def getDSTRFT(self,metadata):
        """
        Devuelve el nivel de distorsión para fertilizante

        Parametros
        ----------
            metadata: str
                String con los metadatos obtenidos de la base de datos.
        Return
        ------
            int:
                Valor de distorsión para fertilizante.
        """

        return np.uint8(int(metadata[self.__DSTRFT_pos[0]:self.__DSTRFT_pos[1]+1],2))  
    
    def getINESTFTFlag(self,metadata):
        """
        Devuelve el valor del flag de INESTABILIDAD PARA FERTILIZANTE

        Parametros
        ----------
            metadata: str
                String con los metadatos obtenidos de la base de datos.
        Return
        ------
                int:
                    Valor del flag de INESTABILIDAD PARA FERTILIZANTE.
        """

        return np.uint8(int(metadata[self.__INESTFTflag_pos[0]:self.__INESTFTflag_pos[1]+1],2))
    
    def getOFFSFT(self,metadata):
        """
        Devuelve el valor del flag de OFFSET PARA FERTILIZANTE

        Parametros
        ----------
            metadata: str
                String con los metadatos obtenidos de la base de datos.
        Return
        ------
                int:
                    Valor del flag de OFFSET PARA FERTILIZANTE.
        """

        return np.uint8(int(metadata[self.__OFFSFT_pos[0]:self.__OFFSFT_pos[1]+1],2))

    def getPMSTFlag(self,metadata):
        """
        Devuelve el valor del flag perdida de muestreo.

        Parametros
        ----------
            metadata: str
                String con los metadatos obtenidos de la base de datos.
        Return
        ------
            int:
                Valor de flag perdida de muestreo.
        """

        return np.uint8(int(metadata[self.__PMSTFlag[0]:self.__PMSTFlag[1]+1],2))
    
    def getGYROX(self,metadata):
        """
        Devuelve el valor del giroscopio en X.

        Parametros
        ----------
            metadata: str
                String con los metadatos obtenidos de la base de datos.
        Return
        ------
                int:
                    Valor del giroscopio en X.
        """

        return np.uint8(int(metadata[self.__GYROX_pos[0]:self.__GYROX_pos[1]+1],2))
    
    def getGYROY(self,metadata):
        """
        Devuelve el valor del giroscopio en Y.

        Parametros
        ----------
            metadata: str
                String con los metadatos obtenidos de la base de datos.
        Return
        ------
                int:
                    Valor del giroscopio en Y.
        """

        return np.uint8(int(metadata[self.__GYROY_pos[0]:self.__GYROY_pos[1]+1],2))
    
    def getGYROZ(self,metadata):
        """
        Devuelve el valor del giroscopio en Z.

        Parametros
        ----------
            metadata: str
                String con los metadatos obtenidos de la base de datos.
        Return
        ------
                int:
                    Valor del giroscopio en Z.
        """

        return np.uint8(int(metadata[self.__GYROZf_pos[0]:self.__GYROZf_pos[1]+1],2))
    
    def getACELX(self,metadata):
        """
        Devuelve el valor del acelerómetro en X.

        Parametros
        ----------
            metadata: str
                String con los metadatos obtenidos de la base de datos.
        Return
        ------
                int:
                    Valor del acelerómetro en X.
        """

        return np.uint8(int(metadata[self.__ACELX_pos[0]:self.__ACELX_pos[1]+1],2))
    
    def getACELY(self,metadata):
        """
        Devuelve el valor del acelerómetro en Y.

        Parametros
        ----------
            metadata: str
                String con los metadatos obtenidos de la base de datos.
        Return
        ------
                int:
                    Valor del acelerómetro en Y.
        """

        return np.uint8(int(metadata[self.__ACELY_pos[0]:self.__ACELY_pos[1]+1],2))
    
    def getACELZ(self,metadata):
        """
        Devuelve el valor del acelerómetro en Z.

        Parametros
        ----------
            metadata: str
                String con los metadatos obtenidos de la base de datos.
        Return
        ------
                int:
                    Valor del acelerómetro en Z.
        """

        return np.uint8(int(metadata[self.__ACELZ_pos[0]:self.__ACELZ_pos[1]+1],2))
    
    def getESTMOFlag(self, metadata):
        """
        Devuelve el valor del flag de ESTMO

        Parametros
        ----------
            metadata: str
                String con los metadatos obtenidos de la base de datos.
        Return
        ------
                int:
                    Valor del flag de ESTMO
        """

        return np.uint8(int(metadata[self.__ESTMOflag_pos[0]:self.__ESTMOflag_pos[1]+1],2))
    
    def getESTORFlag(self, metadata):
        """
        Devuelve el valor del flag de ESTOR

        Parametros
        ----------
            metadata: str
                String con los metadatos obtenidos de la base de datos.
        Return
        ------
                int:
                    Valor del flag de ESTOR
        """

        return np.uint8(int(metadata[self.__ESTORflag_pos[0]:self.__ESTORflag_pos[1]+1],2))
    
    def getSBAT(self, metadata):
        """
        Devuelve el valor del estado de salud de la batería

        Parametros
        ----------
            metadata: str
                String con los metadatos obtenidos de la base de datos.
        Return
        ------
                int:
                    Valor del flag de SBAT
        """

        return np.uint8(int(metadata[self.__SBAT_pos[0]:self.__SBAT_pos[1]+1],2))
    
    def getVBAT(self, metadata):
        """
        Devuelve el valor del voltaje de la batería

        Parametros
        ----------
            metadata: str
                String con los metadatos obtenidos de la base de datos.
        Return
        ------

                int:
                    Valor del flag de VBAT
        """

        return np.uint8(int(metadata[self.__VBAT_pos[0]:self.__VBAT_pos[1]+1],2))
    
    def getCBAT(self, metadata):
        """
        Devuelve el valor del consumo de la batería

        Parametros
        ----------
            metadata: str
                String con los metadatos obtenidos de la base de datos.
        Return
        ------

                int:
                    Valor del flag de CBAT
        """

        return np.uint8(int(metadata[self.__CBAT_pos[0]:self.__CBAT_pos[1]+1],2))
    
    def getESTBMSFlag(self, metadata):
        """
        Devuelve el valor del flag de ESTBMS

        Parametros
        ----------
            metadata: str
                String con los metadatos obtenidos de la base de datos.
        Return
        ------

                int:
                    Valor del flag de ESTBMS
        """

        return np.uint8(int(metadata[self.__ESTBMSflag_pos[0]:self.__ESTBMSflag_pos[1]+1],2))
    
            
    @classmethod
    def getMetadataRevisionNumber(cls):
        """
        Devuelve la versión de los metadatos utilizada.

        Return
        ------
            str:
                Versión de los metadatos utilizada.
        """
        return cls.__metadataVersion
    
if __name__ == "__main__":
    tlmsde = TLMSensorDataExtractor()
    print(tlmsde.getMetadataRevisionNumber())

    sample = np.array(["1010001000010000110000001011000000000000000000001111011010001001",
              "1010001000010000110000001011000000000000000000001111011010001001"])

    tlmsde.getTIMEAC(sample[0])

    # tlmsde.fit(sample)
    print(tlmsde.fit_transform(sample))