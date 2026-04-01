#import "template.typ": *
#import "@preview/codly:1.3.0": *
#show: codly-init.with()

#show: project.with(
  title: "Rapport de Projet de Fin de Module (PFM)",
  authors: (
    (name: "Bilal Houari", email: "houari.bilal@etu.uae.ac.ma", affiliation: "Lisence I.D.A.I."),
  ),
  date: "Avril 1, 2026",
)

#codly(stroke: 0.5pt + gray)



#outline()

#pagebreak(weak: true)

= Introduction
== Aperçu du projet
Le #strong[PreSkool Management System] est une application web intégrée développée en tant qu'exigence académique finale (PFM) pour le module "Développement Backend Avancé en Python". Ce projet représente une application pratique de la logique backend fondamentale et avancée, de la conception de bases de données relationnelles et des principes modernes de développement frontend dans un contexte structuré de gestion scolaire. L'objectif principal du système est de fournir une plateforme centralisée facilitant les processus académiques et administratifs essentiels, garantissant une expérience numérique standardisée tant pour le personnel éducatif que pour les étudiants.

== Objectifs et buts
Le projet visait à établir un système d'information de gestion scolaire intégré capable de gérer les entités de données académiques et administratives fondamentales. Les objectifs opérationnels centraux incluaient la fourniture de capacités de gestion complètes pour les domaines suivants :

- #strong[Gestion des dossiers des étudiants] : Fournir un contrôle administratif complet via des opérations CRUD (Create, Read, Update, Delete) pour les profils des étudiants, englobant l'inscription et la maintenance des données personnelles.
- #strong[Administration du personnel académique] : Développer un module dédié à la gestion des dossiers du corps enseignant, incluant les profils professionnels, les spécialisations par sujet et les affiliations départementales.
- #strong[Organisation curriculaire et départementale] : Établir l'infrastructure administrative nécessaire pour organiser la hiérarchie académique de l'école, spécifiquement à travers la création de départements et leur mise en correspondance ultérieure avec les sujets pertinents.
- #strong[Calendriers des vacances académiques] : Implémenter un système standardisé pour la documentation et le suivi des vacances scolaires et des interruptions programmées au cours de l'année académique.
- #strong[Évaluation et saisie des résultats] : Développer un module pour l'administration des examens scolaires et fournir une interface dédiée au corps enseignant pour enregistrer et surveiller les résultats académiques des étudiants.
- #strong[Sécurité et Role-Based Access Control (RBAC)] : Implémenter un cadre d'authentification structuré avec trois rôles d'utilisateur distincts (Administrator, Teacher et Student), chacun défini par des permissions d'accès spécifiques et des interfaces de dashboard spécialisées.

== Aperçu de la pile technologique (Technology Stack)
L'infrastructure technique du système se compose d'une pile technologique standardisée sélectionnée pour sa stabilité et ses performances :

#figure(
  align(center)[#table(
    columns: 3,
    align: (left, left, left),
    table.header([*Composant*], [*Technologie*], [*Description*]),
    table.hline(),
    [#strong[Backend Framework]],
    [#strong[Django]],
    [Utilisé pour la logique server-side, la gestion de session et la manipulation de données relationnelles via son ORM.],
    [#strong[Database Engine]],
    [#strong[SQLite]],
    [Sélectionné pour sa portabilité et ses performances efficaces au sein de l'environnement de développement.],
    [#strong[Frontend Technologies]],
    [#strong[HTML5, CSS3, JavaScript] (Vanilla)],
    [Outils standards utilisés pour la cohérence visuelle et la maintenabilité sans dépendances à des bibliothèques externes.],
  )],
  kind: table,
)

= Conception et mise en œuvre du système
== Conceptualisation
La conceptualisation du système repose sur un modèle de données relationnel qui organise les opérations scolaires en plusieurs entités fonctionnelles. Chaque entité est définie par ses attributs et ses relations avec les autres composants du système.

=== Gestion de l'identité des utilisateurs et des rôles
Le système utilise un modèle d'utilisateur centralisé pour l'authentification et l'autorisation.

- #strong[Entité `User` de base] : Cette entité utilise l'adresse e-mail comme identifiant principal (username). Elle contient des champs standards tels que le prénom, le nom et le mot de passe.
- #strong[Attribution des rôles] : Un attribut de rôle distingue les utilisateurs en tant qu'Administrator, Teacher ou Student. Cet attribut est utilisé par le système pour déterminer les permissions et les modules de dashboard disponibles.

=== Entités organisationnelles
La hiérarchie académique est établie par les entités `Department` et `Subject`.

- #strong[Départements] : Définis par un nom unique et une description. Ils servent d'unités organisationnelles principales pour les enseignants et les sujets.
- #strong[Matières] : Chaque `Subject` est associé à un `Department` spécifique (relation Many-to-One). Les sujets contiennent un code unique, généré automatiquement à l'aide d'un préfixe dérivé du nom du département et d'un suffixe aléatoire de trois chiffres.

=== Profils du personnel
Le système maintient des dossiers détaillés pour le personnel éducatif via l'entité `Teacher`.

- #strong[Liaison avec l'utilisateur] : Chaque dossier d'enseignant est lié à un compte `User` unique par une relation One-to-One.
- #strong[Identification et attributs] : Un identifiant unique (staff ID, format : STAFF-XXX) est attribué aux enseignants. Les attributs incluent la date de naissance, la spécialisation, la date d'embauche, l'adresse et le numéro de téléphone.
- #strong[Association départementale] : Les enseignants sont liés à un `Subject` spécifique, ce qui les associe par la suite à un `Department`.

=== Profils des étudiants
Les données des étudiants sont gérées via l'entité `Student`, qui suit la progression et le placement individuels.

- #strong[Liaison avec l'utilisateur] : À l'instar des enseignants, chaque dossier d'étudiant est lié à un compte `User` unique via une relation One-to-One.
- #strong[Identification et attributs] : Un numéro d'admission (admission number) unique est attribué aux étudiants, généré automatiquement selon le format ADM-YYYY-XXX. Les attributs incluent la date de naissance, la date d'inscription, l'adresse et le numéro de téléphone.
- #strong[Placement en classe] : Chaque étudiant est affecté à une `SchoolClass` spécifique via une relation Foreign Key.

=== Coordination académique (Classes et affectations)
Les classes et leurs programmes associés sont gérés via les entités `SchoolClass` et `Assignment`.

- #strong[`SchoolClass`] : Définie par un nom unique et un niveau (grade level, allant de 1 à 12). Elle sert de groupement principal pour les étudiants.
- #strong[`ClassSubjectAssignment`] : Cette entité sert de jonction entre `SchoolClass`, `Subject` et `Teacher`. Elle définit quel enseignant est responsable d'un sujet spécifique au sein d'une classe particulière. Une contrainte d'unicité (unique constraint) garantit qu'un sujet ne peut pas être attribué à plus d'un enseignant par classe.

=== Évaluation et performance
Les évaluations sont suivies via les entités `Exam` et `ExamResults`.

- #strong[`Exams`] : Définis par un nom, une date et une note maximale (maximum marks). Chaque examen est lié à un `Subject` et une `SchoolClass` spécifiques.
- #strong[`ExamResults`] : Cette entité enregistre la performance d'un `Student` dans un `Exam` spécifique. Elle stocke les notes obtenues et calcule le pourcentage basé sur la note maximale de l'examen.

== Implémentation
La mise en œuvre du système #strong[PreSkool] utilise une architecture Django modulaire conçue pour l'extensibilité et une séparation claire des préoccupations (#emph[separation of concerns]). Cette section fournit une analyse détaillée des composants techniques, de la logique backend et de l'organisation frontend.

=== Structure des répertoires
Le projet suit une structure modulaire où chaque application représente un domaine fonctionnel distinct. L'arborescence simplifiée ci-dessous met en évidence les composants architecturaux clés, y compris la couche de service (#emph[service layer]) et les outils de gestion.

```text
.
├── admins/
│   └── services.py
├── classes/
│   ├── models.py
│   ├── services.py
│   └── urls.py
├── core/
│   ├── management/commands/seed_data.py
│   ├── mixins.py
│   └── services.py
├── departments/
│   ├── models.py
│   ├── services.py
│   └── urls.py
├── exams/
│   ├── models.py
│   ├── services.py
│   └── urls.py
├── holidays/
│   ├── models.py
│   ├── services.py
│   └── urls.py
├── preskool/                 # Project Settings & Root URLS
├── static/                   # Global Assets (CSS/Images)
├── students/                 # Student Module
│   ├── models.py
│   ├── services.py
│   └── urls.py
├── subjects/                 # Curriculum Module
├── teachers/                 # Personnel Module
├── templates/                # UI Layer (Hierarchical)
│   ├── classes/
│   ├── registration/
│   ├── students/
│   └── (base.html, sidebar.html, topbar.html)
└── users/                    # Authentication and RBAC
```

=== Architecture de la couche de service
Une décision architecturale clé dans ce projet est l'implémentation d'une #strong[Service Layer]. Ce modèle abstrait la logique métier (#emph[business logic]) en dehors des vues, garantissant que les contrôleurs restent légers (#emph[thin controllers]) et que la logique soit réutilisable et testable.

==== Le Service de base (core/services.py)
Tous les services d'application héritent d'un `BaseService`, qui fournit des méthodes standardisées pour les opérations de données de base. Cela garantit que chaque module suit une implémentation cohérente pour les interactions courantes avec la base de données.

```python
class BaseService:
    model = None

    @classmethod
    def get_all(cls):
        """Returns all records for the associated model."""
        return cls.model.objects.all()

    @classmethod
    def get_by_id(cls, obj_id):
        """Retrieves a single record or returns a 404 error."""
        return get_object_or_404(cls.model, id=obj_id)
```

==== Implémentation de services spécialisés (students/services.py)
Le `StudentService` fournit un exemple pratique de la manière dont la couche de service encapsule une logique métier complexe, telle que la génération de numéros d'admission et les affectations de classes.

```python
class StudentService(BaseService):
    model = Student

    @classmethod
    def create_student(cls, user_data, student_data):
        """Handles the dual creation of a User account and a Student profile."""
        with transaction.atomic():
            user = User.objects.create_user(**user_data)
            student = cls.model.objects.create(user=user, **student_data)
        return student

    @classmethod
    def get_class_mates(cls, student_id):
        """Retrieves all students sharing the same class as the specified student."""
        student = cls.get_by_id(student_id)
        if student.school_class:
            return cls.model.objects.filter(school_class=student.school_class)
        return cls.model.objects.none()
```

==== Matrice des responsabilités
Le tableau suivant présente la répartition de la logique métier entre les différents services :

#figure(
  align(center)[#table(
    columns: 3,
    align: (left, left, left),
    table.header([Service], [Exemple de responsabilité], [Implémentation technique]),
    table.hline(),
    [#strong[StudentService]],
    [Gestion des inscriptions],
    [Gère les transactions atomiques lors de la création d'utilisateur/étudiant.],
    [#strong[TeacherService]],
    [Coordination du personnel],
    [Valide les associations de départements via les liaisons de sujets.],
    [#strong[ClassService]], [Cartographie académique], [Gère la table de jonction `ClassSubjectAssignment`.],
    [#strong[ExamService]],
    [Traitement des résultats],
    [Calcule les pourcentages des étudiants en utilisant une précision décimale.],
    [#strong[HolidayService]],
    [Validation du calendrier],
    [Implémente la logique pour vérifier si une date spécifique tombe pendant une pause.],
  )],
  kind: table,
)

=== Implémentation Backend et Entités de Données
L'implémentation backend utilise les modèles #strong[Django] pour définir la structure de données relationnelle du système #strong[PreSkool]. Chaque entité représente un domaine conceptuel spécifique, garantissant que les données sont organisées, validées et gérées par programmation.

==== Identité utilisateur (users/models.py : `CustomUser`)
L'entité `CustomUser` est le modèle d'identité fondamental de l'application. En étendant l'#strong[AbstractUser] de Django, le système maintient la compatibilité avec le cadre d'authentification hérité tout en introduisant une logique spécialisée basée sur les rôles.

- #strong[Objectif fonctionnel] : Elle sert de compte primaire pour tous les individus (Admins, Teachers, Students), gérant l'authentification et l'attribution des niveaux de permission.
- #strong[Contexte relationnel] : Elle agit comme l'entité « Parent » pour les profils `Student` et `Teacher` via des relations #strong[One-to-One].
- #strong[Implémentation] :

```python
class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('TEACHER', 'Teacher'),
        ('STUDENT', 'Student'),
    )
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='STUDENT')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email
        super().save(*args, **kwargs)
```

==== Département institutionnel (departments/models.py : `Department`)
L'entité `Department` organise l'école en unités administratives logiques.

- #strong[Objectif fonctionnel] : Catégoriser les matières académiques et le personnel enseignant dans des domaines d'étude spécifiques (ex: Mathématiques, Sciences).
- #strong[Contexte relationnel] : Elle possède une relation #strong[One-to-Many] avec `Subject` et une relation indirecte avec `Teacher` via leurs matières assignées.
- #strong[Implémentation] :

```python
class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name}"
```

==== Matière académique (subjects/models.py : `Subject`)
L'entité `Subject` définit les cours spécifiques proposés dans le programme.

- #strong[Objectif fonctionnel] : Représenter les cours individuels et gérer leur catégorisation départementale ainsi que leur identification.
- #strong[Contexte relationnel] : Elle appartient à un `Department` (#strong[Foreign Key]) et est liée aux profils `Teacher` en tant que domaine d'expertise principal. Elle apparaît également dans `ClassSubjectAssignment` pour lier les matières à des classes spécifiques.
- #strong[Implémentation] :

```python
class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='subjects')

    def save(self, *args, **kwargs):
        if not self.code:
            dept_prefix = self.department.name[:3].upper()
            random_suffix = ''.join(random.choices(string.digits, k=3))
            self.code = f"{dept_prefix}-{random_suffix}"
            while Subject.objects.filter(code=self.code).exists():
                random_suffix = ''.join(random.choices(string.digits, k=3))
                self.code = f"{dept_prefix}-{random_suffix}"
        super().save(*args, **kwargs)
```

==== Personnel éducatif (teachers/models.py : `Teacher`)
L'entité `Teacher` intègre un profil spécialisé lié à l'identité utilisateur de base pour les données spécifiques au corps enseignant.

- #strong[Objectif fonctionnel] : Gérer les détails du personnel professionnel, incluant l'expertise, l'ancienneté et les marqueurs d'identité.
- #strong[Contexte relationnel] : Liée en #strong[1:1] avec `CustomUser`. Elle possède une relation #strong[Many-to-One] avec `Subject` et apparaît dans plusieurs entrées de `ClassSubjectAssignment`.
- #strong[Implémentation] :

```python
class Teacher(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='teacher_profile')
    staff_id = models.CharField(max_length=20, unique=True, blank=True)
    subject = models.ForeignKey('subjects.Subject', on_delete=models.SET_NULL, null=True, related_name='teachers')
    date_of_birth = models.DateField()
    specialization = models.CharField(max_length=100)
    joining_date = models.DateField(auto_now_add=True)
    address = models.TextField(blank=True)
    phone_number = models.CharField(max_length=15, blank=True)

    def save(self, *args, **kwargs):
        if not self.staff_id:
            random_suffix = ''.join(random.choices(string.digits, k=3))
            self.staff_id = f"STAFF-{random_suffix}"
            while Teacher.objects.filter(staff_id=self.staff_id).exists():
                random_suffix = ''.join(random.choices(string.digits, k=3))
                self.staff_id = f"STAFF-{random_suffix}"
        super().save(*args, **kwargs)
```



==== Classe scolaire (classes/models.py : `SchoolClass`)
L'entité `SchoolClass` facilite le regroupement des étudiants pour l'enseignement académique.

- #strong[Objectif fonctionnel] : Définir les niveaux scolaires et les cohortes administratives au sein de l'institution.
- #strong[Contexte relationnel] : Elle possède une relation #strong[One-to-Many] avec `Student` et sert de clé primaire dans les mappages `ClassSubjectAssignment` et `Exam`.
- #strong[Implémentation] :

```python
class SchoolClass(models.Model):
    name = models.CharField(max_length=50, unique=True)
    grade_level = models.IntegerField() # 1-12
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Class"
        verbose_name_plural = "Classes"
        ordering = ['grade_level', 'name']

    def __str__(self):
        return self.name
```



==== Profils des étudiants (students/models.py : `Student`)
L'entité `Student` représente le profil académique de chaque individu inscrit.

- #strong[Objectif fonctionnel] : Enregistrer les métadonnées spécifiques à l'étudiant et suivre l'affectation en classe.
- #strong[Contexte relationnel] : Liée en #strong[1:1] avec `CustomUser` et appartient à une `SchoolClass` (#strong[Many-to-One]).
- #strong[Implémentation] :

```python
class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student_profile')
    admission_number = models.CharField(max_length=20, unique=True, blank=True)
    date_of_birth = models.DateField()
    school_class = models.ForeignKey('classes.SchoolClass', on_delete=models.SET_NULL, null=True, related_name='students')
    enrollment_date = models.DateField(auto_now_add=True)
    address = models.TextField(blank=True)
    phone_number = models.CharField(max_length=15, blank=True)

    def save(self, *args, **kwargs):
        if not self.admission_number:
            year = datetime.now().year
            random_suffix = ''.join(random.choices(string.digits, k=3))
            self.admission_number = f"ADM-{year}-{random_suffix}"
            while Student.objects.filter(admission_number=self.admission_number).exists():
                random_suffix = ''.join(random.choices(string.digits, k=3))
                self.admission_number = f"ADM-{year}-{random_suffix}"
        super().save(*args, **kwargs)
```

==== Affectations de classe (classes/models.py : `ClassSubjectAssignment`)
L'entité `ClassSubjectAssignment` agit comme la jonction primaire pour l'emploi du temps académique.

- #strong[Objectif fonctionnel] : Coordonner la prestation de matières spécifiques à des classes spécifiques en assignant du personnel enseignant dédié.
- #strong[Contexte relationnel] : Lie `SchoolClass`, `Subject` et `Teacher` via trois #strong[Foreign Keys]. Elle impose une contrainte d'unicité sur la combinaison de la classe et de la matière.
- #strong[Implémentation] :

```python
class ClassSubjectAssignment(models.Model):
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE, related_name='assignments')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='class_assignments')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='class_assignments')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('school_class', 'subject')
        verbose_name = "Class Subject Assignment"
        verbose_name_plural = "Class Subject Assignments"

    def __str__(self):
        return f"{self.school_class.name} - {self.subject.name} ({self.teacher.user.get_full_name()})"
```

==== Planification des examens (exams/models.py : `Exam`)
L'entité `Exam` facilite la programmation des évaluations des étudiants.

- #strong[Objectif fonctionnel] : Définir les paramètres des évaluations académiques, incluant le calendrier et les plafonds de notation.
- #strong[Contexte relationnel] : Liée à `Subject` et `SchoolClass` (#strong[Foreign Keys]). Elle sert d'entité parente pour plusieurs enregistrements `ExamResult`.
- #strong[Implémentation] :

```python
class Exam(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='exams')
    school_class = models.ForeignKey('classes.SchoolClass', on_delete=models.CASCADE, related_name='exams', null=True)
    max_marks = models.IntegerField(default=100)

    def __str__(self):
        return f"{self.name} - {self.subject.name}"
```

==== Résultats académiques (exams/models.py : `ExamResult`)
L'entité `ExamResult` capture la performance des étudiants lors des évaluations.

- #strong[Objectif fonctionnel] : Enregistrer les scores numériques et calculer les pourcentages de performance relative pour chaque étudiant.
- #strong[Contexte relationnel] : Liée à un `Exam` et un `Student` spécifiques (#strong[Foreign Keys]).
- #strong[Implémentation] :

```python
class ExamResult(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='results')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='exam_results')
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.exam.name}: {self.marks_obtained}"

    @property
    def percentage(self):
        if self.exam.max_marks > 0:
            return (self.marks_obtained / self.exam.max_marks) * 100
        return 0
```

==== Calendrier institutionnel (holidays/models.py : `Holiday`)
L'entité `Holiday` maintient le calendrier institutionnel pour les périodes non académiques.

- #strong[Objectif fonctionnel] : Documenter les interruptions et les vacances à l'échelle de l'école.
- #strong[Contexte relationnel] : Il s'agit d'une entité autonome qui fournit un contexte temporel à l'année académique de l'école.
- #strong[Implémentation] :

```python
class Holiday(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.start_date})"

    @property
    def duration(self):
        diff = self.end_date - self.start_date
        return diff.days + 1
```

=== Structure du routage des URL
L'architecture de routage du système #strong[PreSkool] est implémentée à l'aide d'une stratégie décentralisée. Cela implique une configuration à deux niveaux où le projet racine gère les préfixes de domaine de haut niveau et les applications individuelles gèrent leur propre logique de point de terminaison (#strong[endpoint]) localisée.

==== Routage spécifique à l'application
<routage-spécifique-à-lapplication-application-specific-routing>
Chaque application maintient un fichier `urls.py` interne, qui mappe des #strong[patterns] localisés à des vues spécifiques. Cette modularité garantit que la base de code reste organisée et que les modifications apportées à un module n'impactent pas les autres par inadvertance.

*1. Dossiers étudiants et académiques (students/urls.py)*
<1-dossiers-étudiants-et-académiques-studentsurlspy>
Ce routeur gère toutes les interactions spécifiques aux étudiants, allant des vues de #strong[dashboard] à la gestion administrative.

#figure(
  align(center)[#table(
    columns: 3,
    align: (left,left,left,),
    table.header([*Pattern*], [*View Class*], [*Description*],),
    table.hline(),
    [`''`], [`StudentListView`], [Liste globale des étudiants inscrits.],
    [`'dashboard/'`], [`StudentDashboardView`], [Aperçu personnalisé de l'étudiant (Résultats, Camarades de classe).],
    [`'add/'`], [`StudentCreateView`], [Formulaire administratif pour l'inscription des étudiants.],
    [`'edit/<int:pk>/'`], [`StudentUpdateView`], [Modification de profil et maintenance des données.],
    [`'my-class/'`], [`MyClassView`], [Vue de la cohorte de classe assignée à l'étudiant.],
  )]
  , kind: table
  )

*2. Coordination des classes et du programme (classes/urls.py)*\
Le routeur `classes` gère la mise en correspondance des niveaux scolaires et les affectations du corps enseignant à des matières spécifiques.

#figure(
  align(center)[#table(
    columns: 3,
    align: (left,left,left,),
    table.header([*Pattern*], [*View Class*], [*Description*],),
    table.hline(),
    [`''`], [`ClassListView`], [Index de tous les niveaux scolaires actifs.],
    [`'<int:pk>/'`], [`ClassDetailView`], [Analyse approfondie des étudiants d'une classe et des affectations d'enseignants.],
    [`'assignment/add/'`], [`AssignmentCreateView`], [Formulaire spécialisé pour l'affectation d'un enseignant et d'une matière à une classe.],
  )]
  , kind: table
  )

*3. Évaluation et examen (exams/urls.py)*\
Le routage pour le module d'évaluation est conçu pour gérer à la fois la planification et la saisie de données à haut volume requise pour la notation.

#figure(
  align(center)[#table(
    columns: 3,
    align: (left,left,left,),
    table.header([*Pattern*], [*View Class*], [*Description*],),
    table.hline(),
    [`''`], [`ExamListView`], [Liste chronologique des examens programmés.],
    [`'add/'`], [`ExamCreateView`], [Interface pour la planification de nouvelles évaluations.],
    [`'results/entry/<int:exam_id>/'`], [`ExamResultEntryView`], [Portail spécialisé de saisie de données en masse pour la notation par les enseignants.],
  )]
  , kind: table
  )

*4. Programmation institutionnelle et entités (holidays/urls.py)*\
Les applications administratives secondaires (Holidays, Departments, Subjects) suivent un #strong[pattern] de routage #strong[CRUD] standardisé, garantissant la cohérence des conventions de nommage des points de terminaison.

- #strong[Structure de pattern exemple] :
  - `list/` : Pour les aperçus de données.
  - `add/` : Pour la création de nouveaux enregistrements.
  - `edit/<int:pk>/` : Pour la modification d'enregistrements.
  - `delete/<int:pk>/` : Pour la suppression d'enregistrements.

==== Conventions de nommage des URL
Le projet utilise une convention de nommage cohérente (`app-action`) pour chaque route. Cela permet d'obtenir des liens de référence croisée propres, lisibles et maintenables dans toute la couche de #strong[template] en utilisant la balise `{% url %}`.

=== Peuplement des données et automatisation
Le projet inclut un #strong[data seeder] complet situé dans `core/management/commands/seed_data.py`. Cette commande constitue l'une des parties les plus critiques de l'infrastructure de l'application, car elle automatise la création d'un environnement de test complet et réaliste.

#strong[Capacités du Seeder :]

+ #strong[Génération d'identités (Identity Generation)] : Le #strong[seeder] crée un ensemble standard de comptes de test avec des mots de passe fixes (hachage `pbkdf2_sha256`), garantissant que les développeurs peuvent se connecter immédiatement en tant qu'#strong[Admin], #strong[Teacher] ou #strong[Student].
+ #strong[Complexité relationnelle] : Il construit par programmation la hiérarchie académique, en créant d'abord les entités `Department`, suivies des enregistrements `Subject` et `SchoolClass`, garantissant que toutes les contraintes de clés étrangères (#strong[foreign key]) sont respectées.
+ #strong[Peuplement réaliste des données] : À l'aide de boucles et de logiques conditionnelles, il peuple la base de données avec des nombres réalistes d'inscriptions d'étudiants, assigne plusieurs matières aux classes et lie les enseignants en fonction de leurs matières de spécialisation.
+ #strong[Historique académique] : Il génère des événements d'examens (`Exam`) historiques et les enregistrements `ExamResult` correspondants, fournissant des données immédiates pour les #strong[dashboards] de performance.

```python
# core/management/commands/seed_data.py snippet
def handle(self, *args, **options):
    self.stdout.write('Seeding database...')
    # 1. Create Departments
    science = Department.objects.create(name='Science')
    # 2. Create Subjects
    maths = Subject.objects.create(name='Mathematics', department=science)
    # 3. Create Classes
    class_10 = SchoolClass.objects.create(name='Grade 10A', grade_level=10)
    # ... logic continues for Teachers and Students
```

=== Hiérarchie des templates et interface utilisateur
La couche #strong[UI] est organisée en une structure hiérarchique qui maximise la réutilisation du code via l'héritage de #strong[templates] et les #strong[partials].

==== Structure des templates de base
- #strong[`base.html`] : Le layout principal contenant la structure du document HTML et les injections globales de scripts et de styles.
- #strong[`topbar.html`] : Contient le menu du profil utilisateur et les notifications spécifiques aux rôles.
- #strong[`sidebar.html`] : Implémente le menu de navigation rétractable, avec une visibilité des éléments contrôlée par le rôle de l'utilisateur.

==== Consultation des pages spécifiques
Les pages sont regroupées en blocs fonctionnels :

- #strong[Dashboards de gestion] : `student_dashboard.html`, `teacher_dashboard.html`, `home.html` (#strong[dashboard Admin]).
- #strong[Interfaces CRUD] : Formulaires standardisés (`student_form.html`, `exam_form.html`) pour la création et l'édition d'enregistrements.
- #strong[Vues académiques] : `my_class.html` (vue étudiant), `teacher_class_list.html` (vue enseignant) et `exam_result_entry.html`.
- #strong[Listes administratives] : Listes pour les départements, les matières, les vacances et les classes.

==== Stratégie de style (Styling Strategy)
Le style est strictement géré à l'aide de #strong[vanilla CSS], réparti sur trois fichiers pour maintenir une séparation claire des préoccupations (#strong[Layout], #strong[Components] et #strong[Global Variables]).

= Fonctionnalités et caractéristiques clés
Le #strong[PreSkool Management System] intègre plusieurs modules pour traiter les données administratives et académiques. Chaque fonctionnalité est conçue pour automatiser les flux de travail institutionnels et maintenir la cohérence des données sur l'ensemble de la plateforme.

== Data Seeder
Le #strong[Data Seeder] (`seed_data.py`) est un composant administratif central utilisé pour initialiser la base de données du système. Il est conçu à la fois pour les tests de développement et pour les démonstrations du système.

- #strong[Configuration institutionnelle] : Le #strong[seeder] génère la hiérarchie scolaire, incluant les départements, les matières et les niveaux scolaires, en utilisant une seule commande de gestion.
- #strong[Génération de comptes utilisateurs] : Il crée un ensemble standardisé de comptes utilisateurs (#strong[Admin], #strong[Teacher] et #strong[Student]) avec des identifiants prédéfinis.
- #strong[Mappage relationnel] : Le #strong[seeder] implémente des mappages relationnels entre les enseignants, les matières et les classes. Cela inclut la création d'#strong[assignments] et la génération de résultats d'examens pour vérifier la logique du système.
- #strong[Peuplement de données standard] : Il peuple la base de données avec des données synchronisées, telles que l'inscription des étudiants dans des classes spécifiques et les dossiers d'examen correspondants.

== Structure académique et gestion des classes
L'entité #strong[School Class] a été implémentée pour fournir une structure logique pour les étudiants et les programmes.

- #strong[Structure organisationnelle] : Bien que non explicitement requise par les spécifications initiales, le modèle `SchoolClass` a été ajouté pour fournir un mécanisme de regroupement pour les étudiants. Cela prévient les problèmes administratifs qui surviennent lors de la gestion d'étudiants sur plusieurs niveaux scolaires sans une hiérarchie basée sur les classes.
- #strong[Hub administratif] : L'entité classe sert de cible pour les #strong[assignments] matières-enseignants et l'inscription des étudiants.
- #strong[Suivi du niveau scolaire] : Les classes sont regroupées par niveau scolaire (1-12), garantissant que la progression académique des étudiants est enregistrée de manière systématique.

== Dashboards basés sur les rôles
Le système fournit trois interfaces de #strong[dashboard] distinctes basées sur le rôle de l'utilisateur.

- #strong[Administrator Dashboard] : Fournit un accès #strong[CRUD] aux entités du système, incluant le personnel, les départements et les calendriers de vacances.
- #strong[Teacher Dashboard] : Affiche les classes et les matières assignées. Les enseignants peuvent accéder au module de saisie des résultats pour leurs examens.
- #strong[Student Dashboard] : Affiche les #strong[assignments] de classe, les vacances scolaires et les résultats d'examens personnels.

== Gestion du personnel et des programmes
La plateforme gère le personnel scolaire et le programme académique à travers des modules spécialisés.

- #strong[Gestion des enseignants] : Enregistre les spécialisations professionnelles et l'expertise par matière pour les associations enseignants-départements.
- #strong[Organisation du programme] : Les matières sont organisées par département, fournissant une structure pour le programme académique.

== Évaluation et suivi des performances
Le module d'évaluation gère la planification et la notation des évaluations des étudiants.

- #strong[Planification des examens] : Permet la planification des examens pour des matières et des classes spécifiques.
- #strong[Enregistrement des résultats] : Stocke les scores numériques et calcule les pourcentages de performance pour chaque étudiant.

== Calendrier institutionnel
- #strong[Gestion des vacances] : Une interface dédiée pour l'enregistrement des vacances à l'échelle de l'école et des interruptions programmées.

= Défis et solutions
La mise en œuvre du #strong[PreSkool Management System] a été confrontée à plusieurs défis techniques et logistiques qui ont nécessité des ajustements significatifs de l'architecture du projet et de la stratégie de développement.

== Consolidation du périmètre et l'entité SchoolClass
#strong[Défi] : La spécification initiale du projet n'exigeait pas explicitement une entité `SchoolClass` autonome. Au cours de la phase de développement précoce, il est devenu évident que la gestion des étudiants, des matières et des enseignants sans un pôle organisationnel centralisé entraînerait des mappages de données incohérents et un flux de travail administratif désordonné.

#strong[Solution] : Pour éviter cela, l'entité `SchoolClass` a été introduite comme un composant central du modèle de données. Cela a permis de fournir un regroupement logique pour les étudiants et une cible pour les #strong[assignments] matières-enseignants, garantissant ainsi l'intégrité relationnelle du système.

== Mise en œuvre du frontend et contraintes de templates
#strong[Défi] : Un ensemble préexistant de ressources #strong[Bootstrap] avait été initialement fourni pour être utilisé dans le #strong[frontend] du projet. Cependant, ces ressources contenaient une structure de fichiers complexe et redondante, composée de plus de 560 fichiers répartis dans 110 répertoires. Le degré élevé d'imbrication et de duplication rendait difficile l'intégration efficace de ces ressources dans le système d'héritage de #strong[templates Django] dans le délai imparti au projet.

#strong[Solution] : Afin de garantir une base de code propre et maintenable, la décision a été prise de développer une interface utilisateur personnalisée à partir de zéro. Cette approche a permis de mettre en œuvre une structure de #strong[template] plus efficace et un #strong[static asset pipeline] plus léger. Un relevé complet de la structure originale des fichiers de ressources est documenté dans `/report/template-file-tree.md`.

== Sécurité et contrôle d'accès (RBAC)
#strong[Défi] : L'implémentation d'un accès cohérent basé sur les rôles à travers huit applications distinctes nécessitait un mécanisme de sécurité centralisé pour empêcher l'accès non autorisé aux données entre les #strong[Admins], les #strong[Teachers] et les #strong[Students].

#strong[Solution] : Ce problème a été résolu en développant des #strong[mixins] spécialisés dans l'application `core`, tels que `AdminRequiredMixin` et `TeacherRequiredMixin`. Ces #strong[mixins] ont été appliqués à toutes les #strong[class-based views], garantissant que la logique d'autorisation soit appliquée au niveau de la vue avant tout traitement de données.

== Contraintes de temps et d'échéances
Le projet était soumis à des limitations temporelles strictes, avec une date limite de soumission finale fixée au 2 avril 2026. La fenêtre de développement était d'environ 10 jours, durant lesquels tous les modules principaux, la #strong[Service Layer] et l'#strong[UI] personnalisée devaient être entièrement implémentés et testés.

= Défauts et lacunes
Le #strong[PreSkool Management System] a été développé dans un délai restreint de 10 jours pour respecter l'échéance du 2 avril 2026. Par conséquent, l'application se concentre sur les fonctionnalités administratives de base et présente plusieurs lacunes fonctionnelles et techniques qui devraient être corrigées pour un déploiement de niveau production.

== Ensemble limité de fonctionnalités académiques
En raison de la priorité accordée à la gestion de l'identité et des dossiers de base, plusieurs modules académiques avancés n'ont pas été implémentés :

- #strong[Module d'emploi du temps manquant] : Le système ne dispose pas d'un moteur de planification pour gérer les horaires de cours quotidiens, l'attribution des salles et les rotations basées sur les périodes.
- #strong[Absence de gestion des devoirs] : Bien que le système gère les examens formels et les résultats, il ne prend pas actuellement en charge la distribution, la soumission ou la notation des tâches d'évaluation continue (#strong[assignments]).
- #strong[Aucun suivi de l'assiduité] : Les dossiers institutionnels ne comprennent pas de mécanisme pour documenter l'assiduité quotidienne des étudiants ou la présence des enseignants.

== Lacunes institutionnelles et financières
Le périmètre du système a été limité à la gestion académique, laissant d'autres opérations scolaires critiques sans solution :

- #strong[Absence de modules financiers] : Il n'existe aucune fonctionnalité pour la gestion des frais scolaires, de la paie du personnel enseignant ou du suivi des dépenses institutionnelles.
- #strong[Absence de couche de communication] : La plateforme ne facilite pas la communication directe entre les administrateurs, les enseignants et les étudiants (ex : messagerie interne ou systèmes de notification).

== Limitations techniques et de l'interface utilisateur
- #strong[Maturité de l'interface utilisateur] : Bien que l'interface personnalisée en #strong[vanilla CSS] offre une meilleure modularité que le pack de ressources fourni, il s'agit d'une conception de type #strong[Minimum Viable Product (MVP)]. Elle manque de raffinement, d'animations avancées et des fonctionnalités d'accessibilité attendues d'un portail de gestion scolaire de niveau production.
- #strong[Absence de recherche et de filtrage] : L'implémentation actuelle n'inclut aucune fonctionnalité de recherche ou de filtrage. Les utilisateurs doivent identifier manuellement les enregistrements dans les vues de liste administratives, ce qui constitue une limitation majeure pour les systèmes disposant de grands ensembles de données.
- #strong[Absence de pagination] : Tous les enregistrements sont actuellement chargés sur une seule page sans pagination. Cela nécessite l'utilisation du défilement continu (#strong[mousewheel]) et ne constitue pas une solution évolutive pour un usage institutionnel.
- #strong[Génération de rapports et de documents] : Le système ne permet pas de générer des documents officiels, tels que des bulletins de notes au format PDF, des relevés de notes ou des certificats d'inscription.
- #strong[Gestion des médias statiques] : Le système ne prend pas actuellement en charge le téléchargement de fichiers pour les photos de profil des étudiants/enseignants ou le stockage de documents pour les ressources pédagogiques.
- #strong[Moteur de base de données (SQLite)] : Le projet utilise #strong[SQLite] pour la gestion de la base de données. Bien qu'adapté au développement académique, ce moteur n'est pas conçu pour les accès concurrents et les volumes de données requis par un établissement d'enseignement réel.

== Tests et assurance qualité
- #strong[Suite de tests automatisés] : En raison du cycle de développement rapide, le projet n'inclut pas de suite complète de tests unitaires ou d'intégration automatisés. La vérification a été effectuée manuellement à l'aide du #strong[data seeder] pour simuler des environnements institutionnels.

= Conclusion
Le développement du #strong[PreSkool Management System] a abouti à une application backend modulaire et fonctionnelle qui remplit les exigences clés pour la gestion des dossiers à l'échelle de l'école. Malgré le délai strict de 10 jours et les contraintes posées par la structure initiale des ressources, le produit final démontre une implémentation robuste du framework #strong[Django].

== Résultats du projet
Le projet a livré avec succès une plateforme administrative multi-rôles qui gère :

- #strong[Identity Management] : Un accès centralisé basé sur les rôles pour les #strong[Admins], les #strong[Teachers] et les #strong[Students].
- #strong[Academic Hierarchy] : Une organisation complète des départements, des matières et des niveaux scolaires.
- #strong[Dynamic Assessment] : La planification des examens et l'évaluation automatisée des performances.

== Apprentissages et décisions clés
La décision d'implémenter une #strong[Service Layer] personnalisée et une entité #strong[SchoolClass] dédiée s'est avérée essentielle pour maintenir une base de code propre et évolutive. De plus, la construction d'une #strong[Vanilla CSS UI] personnalisée a permis un système d'héritage de #strong[templates] plus efficace et un cycle de développement plus rapide qu'il n'aurait été possible avec le pack de ressources fourni.

== Orientations futures
La version actuelle du système est un modèle de démonstration et ne convient pas à un déploiement dans un environnement institutionnel réel. Pour toute tentative future, des changements significatifs dans la pile technologique seraient nécessaires pour garantir des performances et une évolutivité de niveau production :

- #strong[Frontend Frameworks] : Intégration d'un framework #strong[frontend] dédié (par exemple, #strong[React] ou #strong[Next.js]) pour gérer l'interface utilisateur indépendamment du backend #strong[Django].
- #strong[Production-Grade Database] : Transition de #strong[SQLite] vers un système de gestion de base de données relationnelle robuste tel que #strong[PostgreSQL] pour gérer les utilisateurs concurrents et l'intégrité des données à grande échelle.
- #strong[Advanced Features] : Inclusion de la planification en temps réel (#strong[Timetables]), du suivi des transactions financières (#strong[School Fees]) et de la génération automatisée de documents (#strong[Transcripts]).

En conclusion, le système #strong[PreSkool] sert de #strong[Proof of Concept (POC)] fonctionnel pour un système administratif basé sur #strong[Django], en priorisant le développement modulaire et la structure relationnelle dans un délai limité.


= Captures d'écran

#figure(
  image("assets/Screenshot_2026,04,01_18:59:55.png", height: 32%)
)

#figure(
  image("assets/Screenshot_2026,04,01_19:00:41.png", height: 32%)
)

#figure(
  image("assets/Screenshot_2026,04,01_19:01:22.png", height: 32%)
)

#figure(
  image("assets/Screenshot_2026,04,01_19:01:37.png", height: 32%)
)

#figure(
  image("assets/Screenshot_2026,04,01_19:02:08.png", height: 32%)
)

#figure(
  image("assets/Screenshot_2026,04,01_19:02:19.png", height: 32%)
)

#figure(
  image("assets/Screenshot_2026,04,01_19:02:29.png", height: 32%)
)

#figure(
  image("assets/Screenshot_2026,04,01_19:02:47.png", height: 32%)
)

#figure(
  image("assets/Screenshot_2026,04,01_19:03:38.png", height: 32%)
)

#figure(
  image("assets/Screenshot_2026,04,01_19:03:57.png", height: 32%)
)

#figure(
  image("assets/Screenshot_2026,04,01_19:04:08.png", height: 32%)
)

#figure(
  image("assets/Screenshot_2026,04,01_19:04:18.png", height: 32%)
)

#figure(
  image("assets/Screenshot_2026,04,01_19:04:30.png", height: 32%)
)

#figure(
  image("assets/Screenshot_2026,04,01_19:04:36.png", height: 32%)
)