class EDI837Parser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.segments = []

    def parse_file(self):
        with open(self.file_path, 'r') as file:
            content = file.read()
            self.segments = content.split('~')

    def get_segment_data(self, segment_id):
        return [segment for segment in self.segments if segment.startswith(segment_id)]

    def print_segment(self, segment):
        print(segment.replace('*', ' | '))

    def print_first_segment(self, segment_id, segment_name):
        segments = self.get_segment_data(segment_id)
        if segments:
            print(f"\n{segment_name} ({segment_id}):")
            self.print_segment(segments[0])
        else:
            print(f"\n{segment_name} ({segment_id}) not found.")

    def parse(self):
        self.parse_file()
        
        self.print_first_segment('ISA', 'Interchange Control Header')
        self.print_first_segment('GS', 'Functional Group Header')
        self.print_first_segment('ST', 'Transaction Set Header')
        self.print_first_segment('BHT', 'Beginning of Hierarchical Transaction')
        
        print("\nOther Key Segments:")
        for segment_id, segment_name in [('NM1', 'Individual or Organizational Name'),
                                         ('HL', 'Hierarchical Level'),
                                         ('CLM', 'Claim Information'),
                                         ('SV1', 'Professional Service')]:
            segments = self.get_segment_data(segment_id)
            if segments:
                print(f"\n{segment_name} ({segment_id}) Segments:")
                for segment in segments:
                    self.print_segment(segment)
            else:
                print(f"\n{segment_name} ({segment_id}) segments not found.")


    
if __name__ == "__main__":
    file_path = '/Users/jmodisett/Downloads/CC_837I_EDI.txt'
    parser = EDI837Parser(file_path)
    parser.parse()
