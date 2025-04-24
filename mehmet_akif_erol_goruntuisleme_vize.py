from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
import numpy as np
import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

MARGIN = 10  # pixels
FONT_SIZE = 0.6  # Yazi boyutu kucuk
FONT_THICKNESS = 1
HANDEDNESS_TEXT_COLOR = (88, 205, 54)  # Vibrant green
TEXT_COLOR = (139, 0, 0)  # Koyu mavi (dark blue)
BUTTON_COLOR = (255, 165, 0)  # Turuncu (butonlar icin)

def koordinat_getir(landmarks, indeks, h, w):
    """
    Verilen landmark indeksine ait koordinatlari, resmin genislik ve yuksekligine gore hesaplar.
    """
    landmark = landmarks[indeks]
    return int(landmark.x * w), int(landmark.y * h)

def finger_acik_mi(landmarks, tip, kontrol, h, w):
    """
    Belirtilen parmak icin, referans nokta olarak 0 kullanilarak,
    tip ve kontrol noktasi arasindaki 0'a olan mesafeyi olcer.
    """
    x0, y0 = koordinat_getir(landmarks, 0, h, w)
    x_tip, y_tip = koordinat_getir(landmarks, tip, h, w)
    x_kontrol, y_kontrol = koordinat_getir(landmarks, kontrol, h, w)
    
    mesafe_tip = np.hypot(x_tip - x0, y_tip - y0)
    mesafe_kontrol = np.hypot(x_kontrol - x0, y_kontrol - y0)
    
    return 0 if mesafe_tip < mesafe_kontrol else 1

def basparmak_acik_mi(landmarks, handedness, h, w):
    x_tip, y_tip = koordinat_getir(landmarks, 4, h, w)
    x_eklem1, y_eklem1 = koordinat_getir(landmarks, 2, h, w)
    x_kontrol, y_kontrol = koordinat_getir(landmarks, 5, h, w)
    
    x_avuc, y_avuc = koordinat_getir(landmarks, 9, h, w)
    
    v_x = x_tip - x_eklem1
    v_y = y_tip - y_eklem1

    k_x = x_kontrol - x_eklem1
    k_y = y_kontrol - y_eklem1

    aci = np.arccos((v_x * k_x + v_y * k_y) / 
                    (np.hypot(v_x, v_y) * np.hypot(k_x, k_y) + 1e-6))
    
    mesafe_avuc = np.hypot(x_tip - x_avuc, y_tip - y_avuc)
    mesafe_eklem_avuc = np.hypot(x_eklem1 - x_avuc, y_eklem1 - y_avuc)
    
    aci_derece = np.degrees(aci)
    avuc_yakinlik_orani = mesafe_avuc / (mesafe_eklem_avuc + 1e-6)
    
    if aci_derece > 40 and avuc_yakinlik_orani > 0.8:
        return 1
    return 0

def dort_islem_yap(sayi1, sayi2, islem):
    """
    Verilen iki sayi ve islem tipine gore dort islem yapar.
    """
    if islem == "Toplama":
        return sayi1 + sayi2
    elif islem == "Cikarma":
        return sayi1 - sayi2
    elif islem == "Carpma":
        return sayi1 * sayi2
    elif islem == "Bolme":
        return sayi1 / sayi2 if sayi2 != 0 else "Tanimsiz (Bolme sifira yapilamaz)"
    return None

def is_pointer_inside(x, y, button_x, button_y, button_w, button_h):
    """
    Isaret parmaginin butonun icinde olup olmadigini kontrol eder.
    """
    return button_x <= x <= button_x + button_w and button_y <= y <= button_y + button_h

def draw_landmarks_on_image(rgb_image, detection_result, state, sayi1, sayi2, islem, sonuc, bekleme_sayaci, son_sayi):
    hand_landmarks_list = detection_result.hand_landmarks
    handedness_list = detection_result.handedness
    annotated_image = np.copy(rgb_image)
    h, w, _ = annotated_image.shape

    # Islem Yap butonu (sol ust kose)
    button_x, button_y = 10, 10
    button_w, button_h = 100, 40
    cv2.rectangle(annotated_image, (button_x, button_y), (button_x + button_w, button_y + button_h), BUTTON_COLOR, -1)
    cv2.putText(
        annotated_image,
        "Islem Yap",
        (button_x + 5, button_y + 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        FONT_SIZE,
        TEXT_COLOR,
        FONT_THICKNESS,
        cv2.LINE_AA
    )

    for idx in range(len(hand_landmarks_list)):
        hand_landmarks = hand_landmarks_list[idx]
        handedness = handedness_list[idx]
        parmaklar = []
        
        parmaklar.append(finger_acik_mi(hand_landmarks, 8, 6, h, w))
        parmaklar.append(finger_acik_mi(hand_landmarks, 12, 10, h, w))
        parmaklar.append(finger_acik_mi(hand_landmarks, 16, 14, h, w))
        parmaklar.append(finger_acik_mi(hand_landmarks, 20, 18, h, w))
        parmaklar.append(basparmak_acik_mi(hand_landmarks, handedness, h, w))
        
        toplam_acik = sum(parmaklar)
        x_yaz, y_yaz = koordinat_getir(hand_landmarks, 8, h, w)
        annotated_image = cv2.putText(
            annotated_image,
            str(toplam_acik),
            (x_yaz, y_yaz),
            cv2.FONT_HERSHEY_COMPLEX,
            2,
            (255, 0, 0),
            4
        )

        annotated_image = cv2.circle(annotated_image, (x_yaz, y_yaz), 9, (255, 255, 0), 5)

        hand_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
        hand_landmarks_proto.landmark.extend([
            landmark_pb2.NormalizedLandmark(x=lm.x, y=lm.y, z=lm.z) for lm in hand_landmarks
        ])
        solutions.drawing_utils.draw_landmarks(
            annotated_image,
            hand_landmarks_proto,
            solutions.hands.HAND_CONNECTIONS,
            solutions.drawing_styles.get_default_hand_landmarks_style(),
            solutions.drawing_styles.get_default_hand_connections_style()
        )

        x_coordinates = [lm.x for lm in hand_landmarks]
        y_coordinates = [lm.y for lm in hand_landmarks]
        text_x = int(min(x_coordinates) * w)
        text_y = int(min(y_coordinates) * h) - MARGIN
        cv2.putText(
            annotated_image,
            f"{handedness[0].category_name}",
            (text_x, text_y),
            cv2.FONT_HERSHEY_DUPLEX,
            FONT_SIZE,
            HANDEDNESS_TEXT_COLOR,
            FONT_THICKNESS,
            cv2.LINE_AA
        )

        # Durum bilgisi ve diger bilgileri koyu mavi ile yaz
        cv2.putText(
            annotated_image,
            f"Durum: {state}",
            (10, 70),
            cv2.FONT_HERSHEY_SIMPLEX,
            FONT_SIZE,
            TEXT_COLOR,
            FONT_THICKNESS,
            cv2.LINE_AA
        )

        if state == "Sayi1 Bekleniyor":
            if son_sayi is not None:
                cv2.putText(
                    annotated_image,
                    f"Birinci Sayi: {son_sayi} ({bekleme_sayaci//30} sn)",
                    (10, 100),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    FONT_SIZE,
                    TEXT_COLOR,
                    FONT_THICKNESS,
                    cv2.LINE_AA
                )
        elif state == "Sayi1 Alindi":
            cv2.putText(
                annotated_image,
                f"Birinci Sayi: {sayi1}",
                (10, 100),
                cv2.FONT_HERSHEY_SIMPLEX,
                FONT_SIZE,
                TEXT_COLOR,
                FONT_THICKNESS,
                cv2.LINE_AA
            )
        elif state == "Sayi2 Bekleniyor":
            cv2.putText(
                annotated_image,
                f"Birinci Sayi: {sayi1}",
                (10, 100),
                cv2.FONT_HERSHEY_SIMPLEX,
                FONT_SIZE,
                TEXT_COLOR,
                FONT_THICKNESS,
                cv2.LINE_AA
            )
            if son_sayi is not None:
                cv2.putText(
                    annotated_image,
                    f"Ikinci Sayi: {son_sayi} ({bekleme_sayaci//30} sn)",
                    (10, 130),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    FONT_SIZE,
                    TEXT_COLOR,
                    FONT_THICKNESS,
                    cv2.LINE_AA
                )
        elif state == "Sayi2 Alindi":
            cv2.putText(
                annotated_image,
                f"Birinci Sayi: {sayi1}, Ikinci Sayi: {sayi2}",
                (10, 100),
                cv2.FONT_HERSHEY_SIMPLEX,
                FONT_SIZE,
                TEXT_COLOR,
                FONT_THICKNESS,
                cv2.LINE_AA
            )
            # Islem seceneklerini goster
            operations = ["Toplama", "Cikarma", "Carpma", "Bolme"]
            for i, op in enumerate(operations):
                op_x, op_y = 10, 130 + i * 40
                cv2.rectangle(annotated_image, (op_x, op_y), (op_x + 100, op_y + 30), BUTTON_COLOR, -1)
                cv2.putText(
                    annotated_image,
                    op,
                    (op_x + 5, op_y + 20),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    FONT_SIZE,
                    TEXT_COLOR,
                    FONT_THICKNESS,
                    cv2.LINE_AA
                )
        elif state == "Sonuc":
            cv2.putText(
                annotated_image,
                f"Birinci Sayi: {sayi1}, Ikinci Sayi: {sayi2}, Islem: {islem}",
                (10, 100),
                cv2.FONT_HERSHEY_SIMPLEX,
                FONT_SIZE,
                TEXT_COLOR,
                FONT_THICKNESS,
                cv2.LINE_AA
            )
            cv2.putText(
                annotated_image,
                f"Sonuc: {sonuc}",
                (10, 130),
                cv2.FONT_HERSHEY_SIMPLEX,
                FONT_SIZE,
                TEXT_COLOR,
                FONT_THICKNESS,
                cv2.LINE_AA
            )
            # Main'e Don butonu (yeni koordinatlar)
            main_x, main_y = 500, 10
            cv2.rectangle(annotated_image, (main_x, main_y), (main_x + 100, main_y + 30), BUTTON_COLOR, -1)
            cv2.putText(
                annotated_image,
                "Main'e Don",
                (main_x + 5, main_y + 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                FONT_SIZE,
                TEXT_COLOR,
                FONT_THICKNESS,
                cv2.LINE_AA
            )

    return annotated_image

# HandLandmarker nesnesi olusturma
base_options = python.BaseOptions(model_asset_path='hand_landmarker.task')
options = vision.HandLandmarkerOptions(base_options=base_options, num_hands=2)
detector = vision.HandLandmarker.create_from_options(options)

# Kameradan goruntu alimi ve durum yonetimi
cam = cv2.VideoCapture(0)
state = "Main"  # Durumlar: Main, Sayi1 Bekleniyor, Sayi1 Alindi, Sayi2 Bekleniyor, Sayi2 Alindi, Islem Sec, Sonuc
sayi1 = None
sayi2 = None
islem = None
sonuc = None
bekleme_sayaci = 0
son_sayi = None
BEKLEME_SURESI = 90  # 90 frame (yaklasik 3 saniye)

while cam.isOpened():
    basari, frame = cam.read()
    if basari:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        detection_result = detector.detect(mp_image)
        
        annotated_image = draw_landmarks_on_image(
            mp_image.numpy_view(), detection_result, state, sayi1, sayi2, islem, sonuc, bekleme_sayaci, son_sayi
        )

        if detection_result.hand_landmarks:
            for idx, hand_landmarks in enumerate(detection_result.hand_landmarks):
                handedness = detection_result.handedness[idx]
                h, w, _ = frame.shape
                
                # Isaret parmagi koordinatlari (landmark 8)
                x_isaret, y_isaret = koordinat_getir(hand_landmarks, 8, h, w)

                # Islem Yap butonuna tiklama kontrolu
                if state == "Main":
                    if is_pointer_inside(x_isaret, y_isaret, 10, 10, 100, 40):
                        state = "Sayi1 Bekleniyor"
                        bekleme_sayaci = 0
                        son_sayi = None
                        sayi1 = None
                        sayi2 = None
                        islem = None
                        sonuc = None

                # Birinci sayiyi alma
                if state in ["Sayi1 Bekleniyor", "Sayi2 Bekleniyor"]:
                    if handedness[0].category_name == "Right":  # Sadece sag el ile sayi al
                        parmaklar = []
                        parmaklar.append(finger_acik_mi(hand_landmarks, 8, 6, h, w))
                        parmaklar.append(finger_acik_mi(hand_landmarks, 12, 10, h, w))
                        parmaklar.append(finger_acik_mi(hand_landmarks, 16, 14, h, w))
                        parmaklar.append(finger_acik_mi(hand_landmarks, 20, 18, h, w))
                        parmaklar.append(basparmak_acik_mi(hand_landmarks, handedness, h, w))
                        toplam_acik = sum(parmaklar)

                        if toplam_acik > 0:
                            if son_sayi is None or son_sayi == toplam_acik:
                                son_sayi = toplam_acik
                                bekleme_sayaci += 1
                                if bekleme_sayaci >= BEKLEME_SURESI:
                                    if state == "Sayi1 Bekleniyor":
                                        sayi1 = son_sayi
                                        state = "Sayi1 Alindi"
                                        bekleme_sayaci = 0
                                        son_sayi = None
                                    elif state == "Sayi2 Bekleniyor":
                                        sayi2 = son_sayi
                                        state = "Sayi2 Alindi"
                                        bekleme_sayaci = 0
                                        son_sayi = None
                            else:
                                # Sayi degisti, sayaci sifirla
                                bekleme_sayaci = 0
                                son_sayi = toplam_acik
                        else:
                            bekleme_sayaci = 0
                            son_sayi = None
                    else:
                        bekleme_sayaci = 0
                        son_sayi = None

                # Sayi1 alindiktan sonra Sayi2'yi beklemeye gec
                if state == "Sayi1 Alindi":
                    bekleme_sayaci += 1
                    if bekleme_sayaci >= 30:  # 1 saniye bekle
                        state = "Sayi2 Bekleniyor"
                        bekleme_sayaci = 0

                # Islem secimi
                if state == "Sayi2 Alindi":
                    operations = ["Toplama", "Cikarma", "Carpma", "Bolme"]
                    for i, op in enumerate(operations):
                        op_x, op_y = 10, 130 + i * 40
                        if is_pointer_inside(x_isaret, y_isaret, op_x, op_y, 100, 30):
                            islem = op
                            sonuc = dort_islem_yap(sayi1, sayi2, islem)
                            state = "Sonuc"
                            bekleme_sayaci = 0
                            break  # Islem secildikten sonra donguden cik

                # Main'e Don secenegi (islem seciminden sonra kontrol ediliyor)
                if state == "Sonuc":
                    if is_pointer_inside(x_isaret, y_isaret, 500, 10, 100, 30):
                        state = "Main"
                        sayi1 = None
                        sayi2 = None
                        islem = None
                        sonuc = None
                        bekleme_sayaci = 0
                        son_sayi = None

        cv2.imshow("Image", cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR))
        key = cv2.waitKey(1)
        if key == ord('q') or key == ord('Q'):
            exit(0)

cam.release()
cv2.destroyAllWindows()