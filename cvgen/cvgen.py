def get_letter_template(hiring_manager_name: str,company_name: str, years_of_experience: int,your_name: str):

    letter_template = f"""
    Dear {hiring_manager_name},

    I am writing to express my interest in the Java Developer position at {company_name}. As an experienced Java Developer with {years_of_experience} years of experience, I am confident that I possess the technical expertise, problem-solving abilities, and communication skills needed to excel in this role.

    In my previous positions, I have had the opportunity to work on a wide range of projects, from creating enterprise-level applications to developing software for start-ups. I have experience with Java, Spring Framework, JPA/Hibernate, and SQL databases, as well as experience with agile methodologies and test-driven development. I also have experience with front-end development technologies such as Angular and React, and have used tools like Git and Jenkins to manage the development process.

    One of the reasons I am drawn to {company_name} is your commitment to innovation and cutting-edge technology. I have always been passionate about using technology to solve real-world problems, and I believe that {company_name} is at the forefront of this effort. I am excited about the opportunity to work with a team of talented developers to create solutions that will make a difference in the world.

    Aside from my technical skills, I am a team player who enjoys collaborating with others to achieve common goals. I am always willing to learn from others and to share my own knowledge and experience with my colleagues. In addition, I am a problem solver who is able to work under pressure and meet tight deadlines.

    Thank you for considering my application. I look forward to discussing my qualifications in further detail and learning more about the Java Developer position at {company_name}. Please do not hesitate to contact me if you have any questions or would like to schedule an interview.

    Sincerely,

    {your_name}
    """

    return letter_template

def get_letter_template_in_nl(hiring_manager_name: str,company_name: str, years_of_experience: int,your_name: str):

    letter_template = f"""
    Beste {hiring_manager_name},

    Ik schrijf u om mijn interesse te betuigen in de functie van Java Developer bij {company_name}. Als ervaren Java Developer met {years_of_experience} jaar ervaring ben ik ervan overtuigd dat ik de technische expertise, probleemoplossende vaardigheden en communicatieve vaardigheden bezit die nodig zijn om uit te blinken in deze rol.

    In mijn vorige posities heb ik de kans gehad om aan een breed scala aan projecten te werken, van het creëren van enterprise-level applicaties tot het ontwikkelen van software voor start-ups. Ik heb ervaring met Java, Spring Framework, JPA / Hibernate en SQL-databases, evenals ervaring met agile methoden en testgedreven ontwikkeling. Ik heb ook ervaring met front-end ontwikkelingstechnologieën zoals Angular en React, en heb tools zoals Git en Jenkins gebruikt om het ontwikkelingsproces te beheren.

    Een van de redenen waarom ik aangetrokken ben tot {company_name} is uw toewijding aan innovatie en de nieuwste technologie. Ik ben altijd gepassioneerd geweest door het gebruik van technologie om echte wereldproblemen op te lossen, en ik geloof dat {company_name} aan de voorhoede van deze inspanning staat. Ik kijk ernaar uit om met een team van getalenteerde ontwikkelaars samen te werken om oplossingen te creëren die een verschil zullen maken in de wereld.

    Naast mijn technische vaardigheden ben ik een teamspeler die geniet van het samenwerken met anderen om gemeenschappelijke doelen te bereiken. Ik ben altijd bereid om van anderen te leren en mijn eigen kennis en ervaring met mijn collega's te delen. Daarnaast ben ik een probleemoplosser die in staat is om onder druk te werken en strakke deadlines te halen.

    Bedankt voor het overwegen van mijn sollicitatie. Ik kijk uit naar het bespreken van mijn kwalificaties in meer detail en meer te weten te komen over de functie van Java Developer bij {company_name}. Aarzel niet om contact met mij op te nemen als u vragen heeft of een gesprek wilt plannen.
    
    Met vriendelijke groet,
    
    {your_name}
    
    """

    return letter_template

def get_cv_template(your_name: str, years_of_experience: int, your_skills: list, your_education: list, your_experience: list):
    cv_template = f"""
    {your_name}
    {years_of_experience} years of experience

    Skills
    {''.join([f'{skill}' for skill in your_skills])}
    
    Education
    {''.join([f'{education}' for education in your_education])}
    
    Experience
    {''.join([f'{experience}' for experience in your_experience])}
    
    """
    return cv_template

def main():

    hiring_manager_name = input("Enter Hiring Manager's Name: ")
    company_name = input("Enter Company Name: ")
    years_of_experience = int(input("Enter Number of years of experience: "))
    your_name = input("Enter Your Name: ")

    letter_template = get_letter_template(hiring_manager_name, company_name, years_of_experience, your_name)
    print(letter_template)

    your_skills = []
    your_education = []
    your_experience = []

    while True:
        skill = input("Enter a skill: ")
        your_skills.append(skill)
        if skill == 'q':
            break

    while True:
        education = input("Enter an education: ")
        your_education.append(education)
        if education == 'q':
            break

    while True:
        experience = input("Enter an experience: ")
        your_experience.append(experience)
        if experience == 'q':
            break

    cv_template = get_cv_template(your_name, years_of_experience, your_skills, your_education, your_experience)
    print(cv_template)

if __name__ == '__main__':
    main()
